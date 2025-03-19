from pyrogram import Client, enums
import asyncio
import json
import sys
import os
from dotenv import load_dotenv

class TelegramIDFetcher:
    def __init__(self):
        self.results = {
            'channels': [],
            'groups': [],
            'bots': [],
            'usernames': [],
            'invite_links': []  # Category for invite links
        }

    async def fetch_with_pyrogram(self, invite_links=None):
        """Fetch IDs using Pyrogram"""
        # Load environment variables
        load_dotenv()
        
        # Get credentials from environment variables
        API_ID = os.getenv("API_ID")
        API_HASH = os.getenv("API_HASH")
        SESSION_STRING = os.getenv("SESSION_STRING")
        
        # Check if credentials are available
        if not all([API_ID, API_HASH, SESSION_STRING]):
            print("Error: Missing Telegram API credentials in .env file")
            print("Please create a .env file with API_ID, API_HASH, and SESSION_STRING")
            return False
    
        try:
            print("Connecting to Telegram... (this may take a moment)")
            sys.stdout.flush()  # Force output to be displayed immediately
            
            async with Client(
                name="user",
                api_id=API_ID,
                api_hash=API_HASH,
                session_string=SESSION_STRING,
                in_memory=True
            ) as app:
                print("Connected! Fetching dialogs...")
                sys.stdout.flush()
                
                # Process invite links if provided
                if invite_links and len(invite_links) > 0:
                    print(f"\nProcessing {len(invite_links)} invite links...")
                    sys.stdout.flush()
                    
                    for link in invite_links:
                        try:
                            print(f"\nProcessing invite link: {link}")
                            sys.stdout.flush()
                            
                            # Try to get chat info
                            try:
                                # Extract the invite hash from the link
                                invite_hash = None
                                if '+' in link:
                                    invite_hash = link.split('+')[1]
                                elif 'joinchat/' in link:
                                    invite_hash = link.split('joinchat/')[1]
                                
                                # Try to find the chat in existing dialogs
                                print("Checking if already a member...")
                                sys.stdout.flush()
                                
                                found_in_dialogs = False
                                async for dialog in app.get_dialogs():
                                    chat = dialog.chat
                                    # If we find a matching invite link in chat description or title
                                    if (hasattr(chat, 'invite_link') and chat.invite_link and invite_hash in chat.invite_link) or \
                                       (hasattr(chat, 'description') and chat.description and invite_hash in chat.description):
                                        found_in_dialogs = True
                                        info = {
                                            'title': chat.title or chat.first_name or chat.username or "Unknown",
                                            'username': chat.username if hasattr(chat, 'username') else None,
                                            'id': chat.id,
                                            'type': str(chat.type),
                                            'description': chat.description if hasattr(chat, 'description') else None,
                                            'invite_link': link
                                        }
                                        print(f"Found in existing dialogs: {info['title']} (Type: {chat.type})")
                                        sys.stdout.flush()
                                        
                                        # Add to invite_links category
                                        self.results['invite_links'].append(info)
                                        
                                        # Also categorize based on chat type
                                        if chat.type == enums.ChatType.CHANNEL:
                                            self.results['channels'].append(info)
                                            print("Categorized as: Channel")
                                        elif chat.type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
                                            self.results['groups'].append(info)
                                            print("Categorized as: Group")
                                        break
                                
                                if not found_in_dialogs:
                                    # If not found in dialogs, try to join
                                    print("Not found in existing dialogs. Attempting to join chat...")
                                    sys.stdout.flush()
                                    try:
                                        chat = await app.join_chat(link)
                                        
                                        info = {
                                            'title': chat.title or chat.first_name or chat.username or "Unknown",
                                            'username': chat.username if hasattr(chat, 'username') else None,
                                            'id': chat.id,
                                            'type': str(chat.type),
                                            'description': chat.description if hasattr(chat, 'description') else None,
                                            'invite_link': link
                                        }
                                        
                                        print(f"Successfully joined: {info['title']} (Type: {chat.type})")
                                        sys.stdout.flush()
                                        
                                        # Add to invite_links category
                                        self.results['invite_links'].append(info)
                                        
                                        # Also categorize based on chat type
                                        if chat.type == enums.ChatType.CHANNEL:
                                            self.results['channels'].append(info)
                                            print("Categorized as: Channel")
                                        elif chat.type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
                                            self.results['groups'].append(info)
                                            print("Categorized as: Group")
                                    except Exception as e:
                                        # Check if the error is because we're already a member
                                        if "USER_ALREADY_PARTICIPANT" in str(e):
                                            print("Already a member of this chat. Trying to get chat info directly...")
                                            sys.stdout.flush()
                                            
                                            # Try to get the chat info from the invite hash
                                            try:
                                                # For private groups, we need to use get_chat_history to get a message first
                                                # Then extract the chat from the message
                                                async for dialog in app.get_dialogs():
                                                    chat = dialog.chat
                                                    # Check if this might be our chat by checking recent messages
                                                    try:
                                                        async for message in app.get_chat_history(chat.id, limit=5):
                                                            # If we find a message with our invite link
                                                            if hasattr(message, 'text') and message.text and invite_hash in message.text:
                                                                info = {
                                                                    'title': chat.title or chat.first_name or chat.username or "Unknown",
                                                                    'username': chat.username if hasattr(chat, 'username') else None,
                                                                    'id': chat.id,
                                                                    'type': str(chat.type),
                                                                    'description': chat.description if hasattr(chat, 'description') else None,
                                                                    'invite_link': link
                                                                }
                                                                
                                                                print(f"Found chat through messages: {info['title']} (Type: {chat.type})")
                                                                sys.stdout.flush()
                                                                
                                                                # Add to invite_links category
                                                                self.results['invite_links'].append(info)
                                                                
                                                                # Also categorize based on chat type
                                                                if chat.type == enums.ChatType.CHANNEL:
                                                                    self.results['channels'].append(info)
                                                                    print("Categorized as: Channel")
                                                                elif chat.type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
                                                                    self.results['groups'].append(info)
                                                                    print("Categorized as: Group")
                                                                found_in_dialogs = True
                                                                break
                                                        if found_in_dialogs:
                                                            break
                                                    except Exception:
                                                        continue
                                            except Exception as e2:
                                                print(f"Error getting chat info: {str(e2)}")
                                                sys.stdout.flush()
                                        else:
                                            # If it's a different error, re-raise it
                                            raise e
                            
                            except Exception as e:
                                print(f"Error processing invite link {link}: {str(e)}")
                                sys.stdout.flush()
                                continue
                                
                        except Exception as e:
                            print(f"Error processing invite link {link}: {str(e)}")
                            sys.stdout.flush()
                            continue

                # Remove the hardcoded list of usernames section
                # The following section should be removed:
                # target_usernames = [
                #     "memumssun",
                #     "DebitKard0",
                #     "PandorasTrap",
                #     "RaFORWARDBot",
                #     "RaSCRAPEBot",
                #     "RaSCRAPERChat",
                #     "RaSCRAPER",
                #     "PharaohScraper",
                #     "PharaohScraperChat"
                # ]
                # 
                # print(f"\nSearching for {len(target_usernames)} specific usernames...")
                # for username in target_usernames:
                #     try:
                #         print(f"\nLooking up @{username}")
                #         chat = await app.get_chat(username)
                #         
                #         info = {
                #             'title': chat.title or chat.first_name or chat.username,
                #             'username': chat.username,
                #             'id': chat.id,
                #             'type': str(chat.type),
                #             'description': chat.description if hasattr(chat, 'description') else None
                #         }
                #         
                #         print(f"Found: {info['title']} (Type: {chat.type})")
                #         
                #         # Properly categorize based on chat type
                #         if chat.type == enums.ChatType.CHANNEL:
                #             self.results['channels'].append(info)
                #             print("Categorized as: Channel")
                #         elif chat.type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
                #             self.results['groups'].append(info)
                #             print("Categorized as: Group")
                #         elif chat.type == enums.ChatType.BOT:
                #             self.results['bots'].append(info)
                #             print("Categorized as: Bot")
                #         elif chat.type == enums.ChatType.PRIVATE:
                #             self.results['usernames'].append(info)
                #             print("Categorized as: User")
                #             
                #     except Exception as e:
                #         print(f"Error looking up @{username}: {str(e)}")
                #         continue
                #
                # Remove the hardcoded list of usernames
                # Instead, just fetch all dialogs the user has access to
                
                print("\nFetching all dialogs...")
                async for dialog in app.get_dialogs():
                    try:
                        chat = dialog.chat
                        # Skip if we already have this chat by ID
                        if any(item.get('id') == chat.id for items in self.results.values() for item in items):
                            continue
                            
                        info = {
                            'title': chat.title or chat.first_name or chat.username or "Unknown",
                            'username': chat.username if hasattr(chat, 'username') else None,
                            'id': chat.id,
                            'type': str(chat.type),
                            'description': chat.description if hasattr(chat, 'description') else None
                        }
                        
                        if chat.type == enums.ChatType.CHANNEL:
                            self.results['channels'].append(info)
                            print(f"Found channel: {info['title']}")
                        elif chat.type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
                            self.results['groups'].append(info)
                            print(f"Found group: {info['title']}")
                        elif chat.type == enums.ChatType.BOT:
                            self.results['bots'].append(info)
                            print(f"Found bot: {info['title']}")
                        elif chat.type == enums.ChatType.PRIVATE:
                            self.results['usernames'].append(info)
                            print(f"Found user: {info['title']}")
                    except Exception as e:
                        print(f"Error processing dialog: {e}")
                        continue
                        
        except Exception as e:
            print(f"Error connecting to Telegram: {e}")
            return False
        return True

    def save_results(self):
        """Save results to a JSON file"""
        # Remove invite_links category from final output to avoid duplicates
        results_to_save = {k: v for k, v in self.results.items() if k != 'invite_links'}
        
        with open('telegram_ids.json', 'w', encoding='utf-8') as f:
            json.dump(results_to_save, f, indent=4, ensure_ascii=False)
        print("\nResults have been saved to telegram_ids.json")
        
        try:
            # Also print results to console
            print("\nResults Summary:")
            for category, items in results_to_save.items():
                print(f"\n{category.upper()} ({len(items)} found):")
                for item in items:
                    try:
                        print(f"Title: {item['title']}")
                        if item.get('username'):
                            print(f"Username: @{item['username']}")
                        print(f"ID: {item['id']}")
                        print(f"Type: {item['type']}")
                        if item.get('invite_link'):
                            print(f"Invite Link: {item['invite_link']}")
                        if item.get('description'):
                            print(f"Description: {item['description']}")
                        print("-" * 30)
                    except UnicodeEncodeError:
                        # If we can't print the full title with emojis, try a simplified version
                        print(f"Title: {item['title'].encode('ascii', 'ignore').decode('ascii')} (contains emojis)")
                        if item.get('username'):
                            print(f"Username: @{item['username']}")
                        print(f"ID: {item['id']}")
                        print(f"Type: {item['type']}")
                        if item.get('invite_link'):
                            print(f"Invite Link: {item['invite_link']}")
                        if item.get('description'):
                            print(f"Description: {item['description']}")
                        print("-" * 30)
        except UnicodeEncodeError:
            # If we still have encoding issues, print a simplified version of the results
            print("\nUnicode encoding issue detected. Printing simplified results summary:")
            for category, items in results_to_save.items():
                print(f"\n{category.upper()} ({len(items)} found):")
                for item in items:
                    try:
                        title = item['title'].encode('ascii', 'ignore').decode('ascii')
                        print(f"Title: {title} (original may contain emojis)")
                        if item.get('username'):
                            print(f"Username: @{item['username']}")
                        print(f"ID: {item['id']}")
                        print(f"Type: {item['type']}")
                        print("-" * 30)
                    except:
                        print(f"ID: {item['id']} (Error displaying details)")
                        print("-" * 30)

async def main():
    # Get invite links from command line arguments
    invite_links = []
    if len(sys.argv) > 1:
        for arg in sys.argv[1:]:
            if 't.me/' in arg:
                invite_links.append(arg)
                print(f"Added invite link to process: {arg}")
    
    fetcher = TelegramIDFetcher()
    success = await fetcher.fetch_with_pyrogram(invite_links)
    if success:
        fetcher.save_results()
    else:
        print("Failed to fetch Telegram IDs")

if __name__ == "__main__":
    asyncio.run(main())

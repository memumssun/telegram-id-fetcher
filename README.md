# Telegram ID Fetcher

A powerful tool to fetch IDs and information about Telegram channels, groups, bots, and users that you have access to. This tool is useful for developers working with the Telegram API who need to quickly get the IDs of various Telegram entities.

## Features

- Fetches IDs of all Telegram entities you have access to
- Categorizes entities into channels, groups, bots, and users
- Processes invite links to join and get information about new groups/channels
- Saves results to a JSON file for easy use in other applications
- Handles Unicode characters and emojis in Telegram names

## How It Works

The script connects to your Telegram account using the Pyrogram library and:

1. Processes any invite links provided as command-line arguments
2. Fetches all dialogs (chats) you have access to
3. Categorizes each chat based on its type (channel, group, bot, or user)
4. Saves the results to a JSON file with detailed information about each entity
5. Displays a summary of the results in the console

## Prerequisites

- Python 3.7 or higher
- Required Python packages: `pyrogram`, `tgcrypto`, and `python-dotenv`
- Telegram API credentials (API ID, API Hash, and Session String)

## Installation

### Method 1: Using the Install Script (Windows)

1. Clone or download this repository to your computer
2. Double-click the `install.bat` file to install the required packages
3. Generate your session string (see "Generating Your Session String" section below)
4. Create a `.env` file in the same directory as the script
5. Run the script using 
```bash
python get_telegram_ids.py
```
## Method 2: Manual Installation (Any OS)

1. Clone or download this repository to your computer
2. Open a command prompt or terminal in the project directory
3. Install the required packages by running this script:
```bash
pip install -r requirements.txt
```

4. Generate your session string (see "Generating Your Session String" section below)
5. Create a .env file in the same directory as the script
6. Run the script:
```bash
python get_telegram_ids.py
```

## Getting Your Telegram API Credentials

1. Obtaining API ID and API Hash

1. Visit my.telegram.org and log in with your phone number
2. Click on "API Development Tools"
3. Create a new application by filling in the required fields:
   - App title: Your application name (e.g., "Telegram ID Fetcher")
   - Short name: A short name for your app (e.g., "tg_id_fetcher")
   - Platform: Choose "Desktop"
   - Description: Brief description of your application
4. Click "Create Application"
5. Your API ID (a number) and API HASH (a string) will be displayed
6. Save these credentials - you'll need them for the next step

## 2. Generating Your Session String
This repository includes a script to help you generate a session string:

1. Open the get_session_string.py file in a text editor
2. Replace YOUR_API_ID with your actual API ID (as a number, without quotes)
3. Replace YOUR_API_HASH with your actual API Hash (in quotes)
4. Save the file
5. Run the script:
```bash
python get_session_string.py
```

6. You will be prompted to enter your phone number (with country code, e.g., +12345678901)
7. Enter the verification code sent to your Telegram account
8. If you have two-factor authentication enabled, you'll be asked for your password
9. The script will output your session string - copy this string for the next step
Example of edited get_session_string.py :
```python
from pyrogram import Client

app = Client(
    "my_account",
    api_id=12345678,  # Replace with your actual API ID
    api_hash="abcdef1234567890abcdef1234567890"  # Replace with your actual API Hash
)

async def main():
    async with app:
        session_string = await app.export_session_string()
        print(f"Your session string is: {session_string}")

app.run(main())
 ```
 
 ## Setting Up Your .env File
After obtaining your API credentials and session string, create a .env file:

1. Create a new file named .env in the same directory as the script
2. Add the following content, replacing the placeholder values with your actual credentials:
```plaintext
API_ID=your_api_id_here
API_HASH=your_api_hash_here
SESSION_STRING=your_session_string_here
```

3. Save the file
Example .env file:
```plaintext
API_ID=12345678
API_HASH=abcdef1234567890abcdef1234567890
SESSION_STRING=BQABAAEAcJq4XAACJnNsLV6tYgW9JQQ_lots_of_characters_here
```

## Usage

## Basic Usage
Run the script to fetch all entities you have access to:
```bash
python get_telegram_ids.py
```

## Processing Invite Links
You can also use this tool to join and get information about Telegram groups or channels using invite links:
```bash
python get_telegram_ids.py https://t.me/+ABCDEFGHIJK
```
You can provide multiple invite links at once:
```bash
python get_telegram_ids.py https://t.me/+ABCDEFGHIJK https://t.me/joinchat/LMNOPQRSTUV
```

## Output
The script generates two types of output:

1. Console Output : A summary of all entities found, categorized by type
2. JSON File : A file named telegram_ids.json containing detailed information about each entity
The JSON file has the following structure:
```json
{
    "channels": [
        {
            "title": "Channel Name",
            "username": "channel_username",
            "id": -1001234567890,
            "type": "ChatType.CHANNEL",
            "description": "Channel description"
        },
        ...
    ],
    "groups": [...],
    "bots": [...],
    "usernames": [...]
}
 ```
### Troubleshooting
- If you see errors about TgCrypto, you can ignore them. The script will still work, just a bit slower.
- If you see Unicode encoding errors, the script will still work but some emojis or special characters might not display correctly in the console.
- If you get authentication errors, make sure your API credentials and session string are correct.
- If you're having trouble with the session string, try generating a new one using the get_session_string.py script.

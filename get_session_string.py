from pyrogram import Client

app = Client(
    "my_account",
    api_id=YOUR_API_ID,
    api_hash="YOUR_API_HASH"
)

async def main():
    async with app:
        session_string = await app.export_session_string()
        print(f"Your session string is: {session_string}")

app.run(main())
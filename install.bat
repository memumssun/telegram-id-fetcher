@echo off
echo Installing required packages...
pip install -r requirements.txt
echo.
echo If you see any errors about TgCrypto, you can ignore them.
echo The script will still work, just a bit slower.
echo.
echo IMPORTANT: Before running the script, you need to create a .env file
echo with your Telegram API credentials. See .env.example for the format.
echo.
pause

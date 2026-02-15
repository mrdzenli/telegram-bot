import os
import sys

print("=== DEBUG: Minimal test bot ===")

TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

print(f"DEBUG: BOT_TOKEN={TOKEN}")
print(f"DEBUG: CHAT_ID={CHAT_ID}")

if not TOKEN or not CHAT_ID:
    print("ERROR: BOT_TOKEN или CHAT_ID не заданы!")
    sys.exit(1)

print("SUCCESS: Environment variables are OK. Exiting now.")
sys.exit(0)

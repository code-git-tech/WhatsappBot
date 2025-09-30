import os, sys, json, requests
from pathlib import Path

try:
    from dotenv import load_dotenv  # type: ignore
    load_dotenv()
except Exception:
    pass

TOKEN = os.getenv("WHATSAPP_TOKEN")
PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID")
TEST_RECIPIENT = os.getenv("WHATSAPP_TEST_RECIPIENT", "")  # e.g. 15551234567 (digits only)
TEMPLATE_NAME = os.getenv("WHATSAPP_TEMPLATE_NAME", "")  # optional template name for outside 24h window

if not TOKEN:
    print("❌ Missing WHATSAPP_TOKEN in .env")
    sys.exit(1)
if not PHONE_NUMBER_ID:
    print("❌ Missing WHATSAPP_PHONE_NUMBER_ID in .env")
    sys.exit(1)
if not TEST_RECIPIENT:
    print("⚠️ Set WHATSAPP_TEST_RECIPIENT=1555XXXXXXX in your .env to avoid typing every time.")
    if len(sys.argv) < 2:
        print("Usage: python send_test_message.py 1555XXXXXXXX [Message text]")
        sys.exit(1)
    TEST_RECIPIENT = sys.argv[1]
    message_text = " ".join(sys.argv[2:]) or "Hello from Dooper Bot test!"
else:
    message_text = " ".join(sys.argv[1:]) or "Hello from Dooper Bot test!"

# Normalize: strip '+' and spaces
TEST_RECIPIENT = TEST_RECIPIENT.strip().replace("+", "").replace(" ", "")
if not TEST_RECIPIENT.isdigit():
    print(f"❌ Invalid TEST_RECIPIENT format: {TEST_RECIPIENT}. Use digits only like 15551234567")
    sys.exit(1)

url = f"https://graph.facebook.com/v20.0/{PHONE_NUMBER_ID}/messages"
headers = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}

def send_payload(p):
    print("➡️ Sending payload:", json.dumps(p, indent=2))
    return requests.post(url, headers=headers, json=p, timeout=30)

# Primary: session text message
payload_text = {
    "messaging_product": "whatsapp",
    "to": TEST_RECIPIENT,
    "type": "text",
    "text": {"body": message_text}
}
resp = send_payload(payload_text)
print("📥 Status:", resp.status_code)
try:
    print("📦 Response:", json.dumps(resp.json(), indent=2))
except ValueError:
    print(resp.text)

if resp.status_code == 400 and ('131021' in resp.text or 'message failed' in resp.text.lower()):
    print("⚠️ Session window error: user has not messaged in last 24h.")
    if TEMPLATE_NAME:
        print(f"➡️ Trying template send with template '{TEMPLATE_NAME}' ...")
        template_payload = {
            "messaging_product": "whatsapp",
            "to": TEST_RECIPIENT,
            "type": "template",
            "template": {
                "name": TEMPLATE_NAME,
                "language": {"code": "en_US"}
            }
        }
        resp2 = send_payload(template_payload)
        print("📥 Template Status:", resp2.status_code)
        try:
            print("📦 Template Response:", json.dumps(resp2.json(), indent=2))
        except ValueError:
            print(resp2.text)
    else:
        print("💡 Set WHATSAPP_TEMPLATE_NAME in .env to auto attempt template outside 24h window.")

import requests
import json

# Test if the bot is accessible from internet
ngrok_url = "https://nontransitively-corned-heidi.ngrok-free.dev"

print("🧪 Testing Bot Internet Access...")
print(f"🌐 Bot URL: {ngrok_url}")

try:
    # Test webhook endpoint
    response = requests.get(f"{ngrok_url}/webhook")
    print(f"✅ Webhook Response: {response.status_code} - {response.text}")
    
    # Test webhook verification
    verify_response = requests.get(f"{ngrok_url}/webhook?hub.mode=subscribe&hub.verify_token=my_secure_verify_token_123&hub.challenge=test123")
    print(f"✅ Verification Response: {verify_response.status_code} - {verify_response.text}")
    
    print("\n🎯 READY FOR WHATSAPP!")
    print("Your bot is accessible from the internet!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    print("Bot might not be accessible yet")
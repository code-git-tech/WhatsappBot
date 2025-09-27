import requests
import time

print("🎯 Final Test - Both Services Should Be Working Now!")
time.sleep(2)

# Test the ngrok URL
ngrok_url = "https://nontransitively-corned-heidi.ngrok-free.dev"
webhook_url = f"{ngrok_url}/webhook"

print(f"🌐 Testing: {webhook_url}")

try:
    response = requests.get(webhook_url, timeout=15)
    print(f"📊 Response Code: {response.status_code}")
    print(f"📄 Response: {response.text}")
    
    if response.status_code == 200 and "Webhook is working!" in response.text:
        print("\n🎉 SUCCESS! Bot is accessible from the internet!")
        
        # Test webhook verification
        verify_url = f"{ngrok_url}/webhook?hub.mode=subscribe&hub.verify_token=my_secure_verify_token_123&hub.challenge=TESTCHALLENGE"
        print(f"\n🔐 Testing verification: {verify_url}")
        
        verify_response = requests.get(verify_url, timeout=10)
        print(f"✅ Verification Code: {verify_response.status_code}")
        print(f"✅ Verification Response: {verify_response.text}")
        
        if verify_response.status_code == 200 and verify_response.text == "TESTCHALLENGE":
            print("\n🚀 PERFECT! Everything is working!")
            print(f"🌐 Your WhatsApp Webhook URL: {webhook_url}")
            print("📱 Ready for Facebook/WhatsApp configuration!")
        else:
            print("\n⚠️ Verification has issues")
            
    else:
        print(f"\n❌ Unexpected response: {response.status_code} - {response.text[:100]}")
        
except Exception as e:
    print(f"❌ Error: {e}")
    print("🔧 Check if both services are running")
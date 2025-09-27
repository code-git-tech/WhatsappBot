import requests
import time

print("🔍 Testing Bot Connection (Both Services Running)...")
time.sleep(3)  # Wait for stabilization

# Test the current ngrok URL
ngrok_url = "https://nontransitively-corned-heidi.ngrok-free.dev"

print(f"🌐 Testing: {ngrok_url}")

try:
    # Test webhook endpoint
    webhook_url = f"{ngrok_url}/webhook"
    print(f"🎯 Testing webhook: {webhook_url}")
    
    response = requests.get(webhook_url, timeout=15)
    print(f"📊 Response Code: {response.status_code}")
    print(f"📄 Response Text: {response.text[:200]}")
    
    if response.status_code == 200 and "Webhook is working!" in response.text:
        print("\n🎉 SUCCESS! Bot is online and accessible!")
        print(f"✅ Webhook URL: {webhook_url}")
        
        # Test verification
        verify_url = f"{ngrok_url}/webhook?hub.mode=subscribe&hub.verify_token=my_secure_verify_token_123&hub.challenge=test123"
        verify_response = requests.get(verify_url, timeout=10)
        
        if verify_response.status_code == 200 and verify_response.text == "test123":
            print("✅ Verification: Working!")
            print("\n🎯 READY FOR WHATSAPP CONFIGURATION!")
        else:
            print(f"⚠️ Verification issue: {verify_response.status_code} - {verify_response.text}")
            
    elif "noscript" in response.text and "offline" in response.text:
        print("\n❌ NGROK ERROR: Endpoint is offline")
        print("🔧 Solution: Flask server might not be running properly")
    else:
        print(f"\n⚠️ Unexpected response: {response.status_code}")
        
except Exception as e:
    print(f"❌ Connection failed: {e}")
    print("🔧 Check if both Flask server and ngrok are running")
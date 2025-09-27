#!/usr/bin/env python3
"""
WhatsApp Bot Conversation Tester
This script helps you test and see how conversations will appear in WhatsApp
"""
import requests
import json
import time

def test_whatsapp_conversation():
    print("📱 WHATSAPP BOT CONVERSATION TEST")
    print("=" * 50)
    
    # Your bot details
    bot_url = "http://127.0.0.1:5000"
    phone_number = "+15557667459"
    
    print(f"🤖 Bot Server: {bot_url}")
    print(f"📱 WhatsApp Number: {phone_number}")
    print()
    
    # Test if bot server is running
    try:
        response = requests.get(bot_url, timeout=5)
        print("✅ Bot server is running!")
    except requests.exceptions.RequestException:
        print("❌ Bot server is not running. Start it first:")
        print("   python app.py")
        return
    
    print("\n🎭 SIMULATING WHATSAPP CONVERSATIONS:")
    print("=" * 50)
    
    # Simulate webhook payload from WhatsApp
    test_conversations = [
        {
            "user": "Test User 1",
            "message": "Hi",
            "expected": "Should get greeting message"
        },
        {
            "user": "Test User 2", 
            "message": "1",
            "expected": "Should select Doctor Consultation"
        },
        {
            "user": "Test User 3",
            "message": "Doctor Consultation", 
            "expected": "Should go to appointment options"
        }
    ]
    
    for i, conv in enumerate(test_conversations, 1):
        print(f"\n💬 Test Conversation {i}:")
        print(f"👤 User says: '{conv['message']}'")
        print(f"🤖 Expected: {conv['expected']}")
        
        # Simulate WhatsApp webhook payload
        webhook_payload = {
            "entry": [{
                "changes": [{
                    "value": {
                        "messages": [{
                            "from": f"test_user_{i}",
                            "text": {"body": conv['message']}
                        }]
                    }
                }]
            }]
        }
        
        try:
            # Send to your bot's webhook
            response = requests.post(
                f"{bot_url}/webhook",
                json=webhook_payload,
                timeout=10
            )
            
            if response.status_code == 200:
                print("✅ Bot processed message successfully")
            else:
                print(f"❌ Bot error: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Connection error: {e}")
        
        time.sleep(1)  # Small delay between tests
    
    print(f"\n📱 TO SEE THESE CONVERSATIONS IN YOUR WHATSAPP APP:")
    print("=" * 50)
    print("1. Make sure you have real WhatsApp API credentials in .env")
    print("2. Your bot server must be accessible from internet (use ngrok)")
    print("3. Send actual messages to +15557667459 from any WhatsApp")
    print("4. Conversations will appear in the WhatsApp Business app")
    print()
    print("🎯 WHAT YOU'LL SEE IN WHATSAPP:")
    print("• User sends: 'Hi'")
    print("• Bot replies: 'Greetings and welcome to Dooper Health!'")
    print("• Bot shows menu: 1. Doctor Consultation, 2. Book Lab Test, etc.")
    print("• User selects option → Bot continues conversation flow")

if __name__ == "__main__":
    test_whatsapp_conversation()
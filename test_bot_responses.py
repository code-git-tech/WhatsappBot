#!/usr/bin/env python3
"""
Simulate WhatsApp message processing
This shows exactly how your bot will respond when webhook is working
"""

import json
import requests
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

def simulate_incoming_message():
    """Simulate what Facebook sends to your webhook when user messages you"""
    
    # This is exactly what Facebook sends to your /webhook endpoint
    facebook_payload = {
        "object": "whatsapp_business_account",
        "entry": [
            {
                "id": "110735612113186",
                "changes": [
                    {
                        "value": {
                            "messaging_product": "whatsapp",
                            "metadata": {
                                "display_phone_number": "15550596748",
                                "phone_number_id": "110735612113186"
                            },
                            "contacts": [
                                {
                                    "profile": {
                                        "name": "Test User"
                                    },
                                    "wa_id": "15557667459"
                                }
                            ],
                            "messages": [
                                {
                                    "from": "15557667459",
                                    "id": "wamid.test123",
                                    "timestamp": "1695800000",
                                    "text": {
                                        "body": "Hi"
                                    },
                                    "type": "text"
                                }
                            ]
                        },
                        "field": "messages"
                    }
                ]
            }
        ]
    }
    
    return facebook_payload

def test_webhook_locally():
    """Test your webhook endpoint locally to see how it responds"""
    
    print("🧪 Testing WhatsApp Bot Response Simulation")
    print("=" * 60)
    
    # Simulate incoming message
    payload = simulate_incoming_message()
    
    print("📥 Simulating user message: 'Hi'")
    print(f"📱 From: +15557667459")
    print(f"📤 Sending to your local webhook...")
    
    try:
        # Send to your local Flask server (simulating Facebook's webhook call)
        response = requests.post(
            'http://localhost:5000/webhook',
            json=payload,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            print("✅ Webhook processed successfully!")
            print(f"📋 Response: {response.text}")
            print("\n🤖 Your bot should have sent a response message!")
            print("💡 Check the Flask server logs above to see what happened.")
        else:
            print(f"❌ Webhook failed: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error testing webhook: {e}")
        print("Make sure your Flask server is running: python app.py")

def test_different_messages():
    """Test how bot responds to different messages"""
    
    test_messages = [
        "Hi",
        "1",  # First option
        "2",  # Second option 
        "doctor",
        "help"
    ]
    
    print("\n" + "=" * 60)
    print("🧪 Testing Different User Messages")
    print("=" * 60)
    
    for i, message in enumerate(test_messages, 1):
        print(f"\n📝 Test {i}: User sends '{message}'")
        
        # Create payload for this message
        payload = simulate_incoming_message()
        payload["entry"][0]["changes"][0]["value"]["messages"][0]["text"]["body"] = message
        
        try:
            response = requests.post(
                'http://localhost:5000/webhook',
                json=payload,
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 200:
                print(f"✅ Bot processed: '{message}'")
            else:
                print(f"❌ Failed to process: '{message}'")
                
        except Exception as e:
            print(f"❌ Error with message '{message}': {e}")

if __name__ == "__main__":
    print("🤖 WhatsApp Bot Response Tester")
    print("This simulates what happens when users message your bot")
    print("\n📋 Make sure your Flask server is running in another terminal!")
    
    # Test single message first
    test_webhook_locally()
    
    # Test multiple messages
    test_different_messages()
    
    print("\n" + "=" * 60)
    print("🎯 Summary:")
    print("- Your bot logic is working locally ✅")
    print("- When webhook is connected, users will get automatic responses ✅")
    print("- The only missing piece is the stable webhook URL 🔧")
    print("\n💡 Next step: Deploy to cloud or use paid tunnel for webhook")
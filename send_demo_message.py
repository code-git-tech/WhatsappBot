#!/usr/bin/env python3
"""
Test WhatsApp API - Send actual message to show bot capabilities
"""

import requests
import json
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

WHATSAPP_TOKEN = os.getenv('WHATSAPP_TOKEN')
WHATSAPP_PHONE_NUMBER_ID = os.getenv('WHATSAPP_PHONE_NUMBER_ID')
WHATSAPP_API_URL = f'https://graph.facebook.com/v18.0/{WHATSAPP_PHONE_NUMBER_ID}/messages'

def send_demo_message():
    """Send a demo message showing how the bot will work"""
    
    # Your test number
    test_phone = "15557667459"
    
    # Demo message showing bot capabilities
    demo_message = """🤖 DOOPER MEDICAL BOT - DEMO

✅ Your WhatsApp bot is working!

When webhook is connected, here's how conversations will work:

👤 User: "Hi"
🤖 Bot: "Please choose a service:
1. Doctor Consultation  
2. Book Lab Test
3. Order Medicine
4. Home Care
5. Home Vaccination
6. Other Query"

👤 User: "1" 
🤖 Bot: Shows doctor booking form

👤 User: "3"
🤖 Bot: "Upload prescription or type medicine names"

🔧 Current Status:
✅ Bot logic: Working
✅ API connection: Working  
✅ Message processing: Working
⚠️ Webhook: Needs stable URL

💡 Next: Deploy to cloud or use paid tunnel for full functionality!"""

    message_data = {
        "messaging_product": "whatsapp",
        "to": test_phone,
        "type": "text",
        "text": {"body": demo_message}
    }
    
    headers = {
        'Authorization': f'Bearer {WHATSAPP_TOKEN}',
        'Content-Type': 'application/json'
    }
    
    try:
        print("📤 Sending demo message to show bot capabilities...")
        response = requests.post(WHATSAPP_API_URL, json=message_data, headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            message_id = result.get('messages', [{}])[0].get('id')
            print(f"✅ Demo message sent successfully!")
            print(f"📱 Message ID: {message_id}")
            print(f"📞 Check WhatsApp at +{test_phone}")
            return True
        else:
            print(f"❌ Failed to send message")
            print(f"Status Code: {response.status_code}")
            print(f"Response: {response.text}")
            
            if response.status_code == 400:
                error_data = response.json()
                if "131030" in str(error_data):
                    print("\n🔧 FIX NEEDED: Add your number to Facebook recipient list!")
                    print("1. Go to Facebook Developer Console")
                    print("2. WhatsApp > Getting Started")  
                    print("3. Add +15557667459 to recipient phone numbers")
                    print("4. Verify the number when Facebook sends code")
            
            return False
            
    except Exception as e:
        print(f"❌ Error sending message: {str(e)}")
        return False

if __name__ == "__main__":
    print("🤖 WhatsApp Bot Demo Message Sender")
    print("=" * 50)
    
    if send_demo_message():
        print("\n🎉 Success! Check your WhatsApp!")
    else:
        print("\n❌ Demo message failed. Check error above.")
    
    print("\n" + "=" * 50)
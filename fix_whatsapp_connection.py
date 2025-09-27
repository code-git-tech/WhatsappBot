#!/usr/bin/env python3
"""
WhatsApp Bot Connection Fix
This script helps you connect your bot so it responds to messages on +15557667459
"""

def fix_whatsapp_bot_connection():
    print("🔧 FIXING WHATSAPP BOT CONNECTION")
    print("=" * 60)
    print("Your bot isn't responding because it's not connected to WhatsApp servers")
    print()
    
    print("❌ CURRENT PROBLEM:")
    print("• Your bot runs on localhost:5000 (only your computer)")
    print("• WhatsApp servers can't reach your computer")
    print("• Messages to +15557667459 don't reach your bot")
    print()
    
    print("✅ SOLUTION - 3 STEPS:")
    print("=" * 40)
    
    print("\n1️⃣ GET REAL WHATSAPP API CREDENTIALS:")
    print("   Go to: https://developers.facebook.com/")
    print("   • Create WhatsApp Business API app")
    print("   • Add your phone +15557667459") 
    print("   • Get these values:")
    print("     - Access Token (EAA...)")
    print("     - Phone Number ID (16 digits)")
    print("     - Verify Token (you create this)")
    
    print("\n2️⃣ EXPOSE YOUR BOT TO INTERNET:")
    print("   Download ngrok: https://ngrok.com/download")
    print("   • Extract ngrok.exe to your bot folder")
    print("   • Run: ngrok http 5000")
    print("   • Copy the https://xxx.ngrok.io URL")
    
    print("\n3️⃣ CONNECT WEBHOOK:")
    print("   In Facebook Developers console:")
    print("   • Set Webhook URL: https://xxx.ngrok.io/webhook")
    print("   • Set Verify Token: (same as in your .env)")
    print("   • Subscribe to 'messages' events")
    
    print("\n" + "=" * 60)
    print("🎯 STEP-BY-STEP QUICK FIX:")
    print("=" * 60)
    
    print("\nSTEP 1: Start your bot server")
    print("   python app.py")
    
    print("\nSTEP 2: Download & run ngrok")
    print("   1. Go to https://ngrok.com/download")
    print("   2. Download ngrok for Windows")
    print("   3. Extract ngrok.exe to C:\\Users\\sarve\\Desktop\\bot\\")
    print("   4. Open new terminal and run: .\\ngrok http 5000")
    print("   5. Copy the https URL (like https://abc123.ngrok.io)")
    
    print("\nSTEP 3: Update Facebook webhook")
    print("   1. Go to https://developers.facebook.com/")
    print("   2. Find your WhatsApp app")
    print("   3. Go to WhatsApp > Configuration")
    print("   4. Set Webhook URL: https://abc123.ngrok.io/webhook")
    print("   5. Set Verify Token: test_verify_token")
    
    print("\nSTEP 4: Update your .env file")
    print("   Replace with real values:")
    print("   WHATSAPP_TOKEN=EAAyour_real_token")
    print("   WHATSAPP_VERIFY_TOKEN=test_verify_token")
    
    print("\nSTEP 5: Test")
    print("   Send 'Hi' to +15557667459 from any WhatsApp")
    print("   Should get: 'Greetings and welcome to Dooper Health!'")
    
    print("\n" + "=" * 60)
    print("🚀 AFTER SETUP:")
    print("Messages to +15557667459 → WhatsApp API → Your ngrok URL → Your bot → Response")
    print()
    print("📱 YOU'LL SEE:")
    print("• Messages in WhatsApp Business app")
    print("• Automatic bot responses")
    print("• Medical consultation flow from your JSON")
    
    print("\n💡 ALTERNATIVE - ONLINE BOT HOSTING:")
    print("Instead of ngrok, you can deploy to:")
    print("• Heroku (free tier)")
    print("• Railway")
    print("• Render")
    print("• DigitalOcean")

if __name__ == "__main__":
    fix_whatsapp_bot_connection()
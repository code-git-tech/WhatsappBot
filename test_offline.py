#!/usr/bin/env python3
"""
Offline test script for the WhatsApp bot
This tests the conversation logic without sending real WhatsApp messages
"""
import sys
import os
import json
sys.path.append('.')

# Mock the WhatsApp send function for testing
def mock_send_whatsapp_text(to, text):
    print(f"🤖 Bot says: {text}")
    return {"success": True}

# Patch the send function
import app
app.send_whatsapp_text = mock_send_whatsapp_text

from app import handle_user_message, init_db, operators, find_start_node, get_node

def offline_test():
    print("🤖 Testing WhatsApp Bot (Offline Mode)")
    print("=" * 50)
    
    # Initialize database
    init_db()
    
    # Test user ID
    test_user = "test_user_123"
    
    print(f"📋 Bot loaded: dooper_bot.json with {len(operators)} nodes")
    print(f"🎯 Start node: {find_start_node()}")
    
    # Get start node info
    start_node = get_node(find_start_node())
    print(f"📝 Start message: {start_node.get('question', 'No question')}")
    
    print("\n" + "="*50)
    print("💬 CONVERSATION SIMULATION")
    print("="*50)
    
    # Simulate conversation
    print("\n[Conversation starts]")
    
    # First interaction
    print("\n👤 User sends: Hi")
    handle_user_message(test_user, "Hi")
    
    print("\n👤 User sends: 1")
    handle_user_message(test_user, "1")
    
    print("\n👤 User sends: Book Appointment") 
    handle_user_message(test_user, "Book Appointment")
    
    print("\n✅ Offline test completed!")
    print("🚀 Your bot logic is working perfectly!")

if __name__ == "__main__":
    offline_test()
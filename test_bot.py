#!/usr/bin/env python3
"""
Test script for the WhatsApp bot
This simulates a user conversation without needing real WhatsApp API
"""
import sys
import os
sys.path.append('.')

# Import bot functions
from app import handle_user_message, init_db, operators, find_start_node, get_node

def test_bot():
    print("🤖 Testing WhatsApp Bot Locally")
    print("=" * 50)
    
    # Initialize database
    init_db()
    
    # Test user ID
    test_user = "test_user_123"
    
    print(f"📋 Bot has {len(operators)} conversation nodes loaded")
    print(f"🎯 Start node: {find_start_node()}")
    
    # Simulate conversation
    print("\n💬 Starting conversation...")
    
    # First message - should trigger start node
    print("\n👤 User: Hi")
    handle_user_message(test_user, "Hi")
    
    print("\n👤 User: 1 (Doctor Consultation)")
    handle_user_message(test_user, "1")
    
    print("\n👤 User: Book Appointment")
    handle_user_message(test_user, "Book Appointment")
    
    print("\n✅ Test completed! Check the output above.")
    print("📝 Note: In real usage, messages would be sent via WhatsApp API")

if __name__ == "__main__":
    test_bot()
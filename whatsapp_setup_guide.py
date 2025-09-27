# WhatsApp Business API Setup Guide
# ====================================

# 1. Go to: https://developers.facebook.com/
# 2. Create a new app or use existing app
# 3. Add "WhatsApp Business API" product
# 4. Go to WhatsApp > API Setup

# You'll need these values:
# 
# WHATSAPP_TOKEN = "Your permanent access token from Facebook Developers"
# Example: EAABm9rJbaAkBOxxxxxxxxxxxxxxxxxxxxxxxxxx
#
# WHATSAPP_PHONE_NUMBER_ID = "Your phone number ID (NOT the phone number itself)"  
# Example: 1234567890123456 (this is different from +15557667459)
#
# WHATSAPP_VERIFY_TOKEN = "A secret string you create for webhook verification"
# Example: my_secret_verify_token_12345

# Steps to find your Phone Number ID:
# 1. In Facebook Developers console
# 2. Go to WhatsApp > API Setup  
# 3. Look for your phone number +15557667459
# 4. Copy the "Phone number ID" (long number like 1234567890123456)

print("Follow the instructions above to get your WhatsApp API credentials")
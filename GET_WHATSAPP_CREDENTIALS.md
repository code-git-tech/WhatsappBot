# 🔑 HOW TO GET REAL WHATSAPP API CREDENTIALS

## 📋 STEP-BY-STEP GUIDE:

### STEP 1: Go to Facebook Developers

1. Open browser: **https://developers.facebook.com/**
2. Click **"Log In"** (use your Facebook account)
3. If you don't have Facebook account, create one first

### STEP 2: Create or Find Your App

**Option A - If you already have an app:**

1. Click **"My Apps"** in top menu
2. Select your existing WhatsApp Business app

**Option B - If you need to create new app:**

1. Click **"Create App"**
2. Choose **"Business"**
3. Enter app name (e.g., "My WhatsApp Bot")
4. Enter your email
5. Click **"Create App"**

### STEP 3: Add WhatsApp Product

1. In your app dashboard, look for **"Add Products to Your App"**
2. Find **"WhatsApp"** and click **"Set up"**
3. If already added, click **"WhatsApp"** in left sidebar

### STEP 4: Get Your Access Token

1. In WhatsApp section, go to **"API Setup"**
2. Look for **"Temporary access token"**
3. Click **"Copy"** button next to the token
4. **SAVE THIS TOKEN** - starts with `EAA...`

### STEP 5: Get Your Phone Number ID

1. Still in **"API Setup"** section
2. Look for **"From phone number ID"**
3. Copy the **16-digit number**
4. **SAVE THIS ID**

### STEP 6: Add Your Phone Number

1. In WhatsApp section, go to **"Phone Numbers"**
2. Click **"Add phone number"**
3. Enter **+15557667459**
4. Follow verification steps

## 📝 WHAT YOU'LL GET:

**Access Token** (example):

```
EAA123ABC456DEF789GHI012JKL345MNO678PQR901STU234VWX567YZ890
```

**Phone Number ID** (example):

```
1234567890123456
```

## 🔄 UPDATE YOUR .ENV FILE:

Once you have these, replace in your `.env` file:

```
WHATSAPP_TOKEN=EAA123ABC456DEF789GHI012JKL345MNO678PQR901STU234VWX567YZ890
WHATSAPP_PHONE_NUMBER_ID=1234567890123456
```

## ❗ IMPORTANT NOTES:

- **Temporary tokens expire in 24 hours** - for production, you'll need permanent token
- **Phone number must be verified** with Facebook
- **Keep credentials secure** - don't share them publicly

## 🆘 IF YOU GET STUCK:

- **No Facebook account?** Create one at facebook.com first
- **Can't find WhatsApp option?** Make sure your app type is "Business"
- **Phone verification fails?** Use a real phone number you control
- **Need help?** Facebook has detailed docs at developers.facebook.com/docs/whatsapp

## 📱 NEXT STEP:

After getting credentials, I'll help you:

1. Update your .env file
2. Configure the webhook
3. Test your bot with real WhatsApp messages!

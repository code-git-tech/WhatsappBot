# WhatsApp Webhook Configuration Guide

## ⚠️ API Version Consistency

Facebook requires using the **SAME API VERSION** for all webhook subscriptions to ensure reliable updates.

### ✅ Correct Configuration

**Use API Version: v18.0** (Latest stable)

## 🔧 Webhook Configuration Steps

### 1. In Facebook Developer Console

**Navigate to:**

- Facebook Developer Console → Your App → WhatsApp → Configuration

### 2. Webhook Settings

**Callback URL:**

```
https://your-stable-url.com/webhook
```

**Verify Token:**

```
1285389302894210
```

**API Version: v18.0** ⭐ (Important: Use same version everywhere)

### 3. Webhook Fields Subscription

Subscribe to these fields with **v18.0**:

✅ **Required:**

- `messages` (v18.0)

✅ **Optional but Recommended:**

- `message_deliveries` (v18.0)
- `message_reads` (v18.0)
- `message_reactions` (v18.0)

❌ **Don't Mix Versions:**

- ~~messages (v16.0)~~
- ~~message_deliveries (v17.0)~~
- This causes the warning you're seeing!

## 📋 Configuration Checklist

### Before Configuring Webhook:

1. ✅ **Get Stable URL**

   - Deploy to Railway/Heroku/Cloud service
   - OR use ngrok Pro with custom domain
   - OR use paid tunnel service

2. ✅ **Ensure Flask Server is Running**

   ```bash
   python app.py
   ```

3. ✅ **Test Webhook Locally First**
   ```bash
   curl "https://your-url.com/webhook?hub.verify_token=1285389302894210&hub.challenge=test&hub.mode=subscribe"
   ```
   Should return: `test`

### Configuration Form Values:

```
┌─────────────────────────────────────────┐
│  Webhook Configuration (v18.0)          │
├─────────────────────────────────────────┤
│                                         │
│  Callback URL:                          │
│  https://your-app.railway.app/webhook   │
│                                         │
│  Verify Token:                          │
│  1285389302894210                       │
│                                         │
│  Webhook Fields (ALL v18.0):            │
│  ☑️ messages                            │
│  ☑️ message_deliveries                  │
│  ☑️ message_reads                       │
│                                         │
│  API Version: v18.0 ⭐                  │
│                                         │
│  [Verify and Save]                      │
└─────────────────────────────────────────┘
```

## 🚀 Quick Deploy Options

### Option 1: Railway (Recommended - Free)

1. **Create requirements.txt:**

```
flask==3.0.0
python-dotenv==1.0.0
requests==2.31.0
```

2. **Push to GitHub:**

```bash
git init
git add .
git commit -m "WhatsApp Medical Bot v18.0"
git push origin main
```

3. **Deploy on Railway:**

- Go to https://railway.app
- Connect GitHub → Deploy
- Set environment variables
- Get URL: `https://your-app.railway.app`

### Option 2: Heroku

```bash
heroku create whatsapp-medical-bot
heroku config:set WHATSAPP_TOKEN=your_token
heroku config:set WHATSAPP_PHONE_NUMBER_ID=110735612113186
heroku config:set WHATSAPP_VERIFY_TOKEN=1285389302894210
git push heroku main
```

## 🔍 Troubleshooting

### "API version consistency" warning:

- ✅ **Solution:** Use v18.0 for ALL webhook subscriptions
- ❌ **Problem:** Mixed versions (v16.0 + v17.0 + v18.0)

### "Callback URL validation failed":

- Check if URL is accessible: `curl https://your-url.com/webhook`
- Verify Flask server is running
- Ensure tunnel/deployment is stable

### "Verify token mismatch":

- Double-check token: `1285389302894210`
- Ensure no extra spaces in token field

## ✅ Success Indicators

When properly configured, you should see:

- ✅ Green checkmark next to webhook URL
- ✅ "Webhook verified successfully" message
- ✅ No API version warnings
- ✅ Messages flow: User → WhatsApp → Bot → Response

## 🎯 Final Configuration Summary

1. **API Version:** v18.0 (everywhere)
2. **Callback URL:** https://your-stable-url.com/webhook
3. **Verify Token:** 1285389302894210
4. **Subscriptions:** messages, message_deliveries, message_reads (all v18.0)
5. **Test:** Send "Hi" to +15557667459 → Bot responds automatically

# Quick Deploy to Railway (Free & Fast)

## 1. Create GitHub Repository

```bash
git init
git add .
git commit -m "WhatsApp Medical Bot"
git remote add origin https://github.com/yourusername/whatsapp-medical-bot
git push -u origin main
```

## 2. Create requirements.txt

```
flask==3.0.0
python-dotenv==1.0.0
requests==2.31.0
```

## 3. Deploy on Railway

- Go to https://railway.app
- Sign up with GitHub
- "New Project" → "Deploy from GitHub"
- Select your repository
- Railway will give you: https://your-app.railway.app

## 4. Set Environment Variables in Railway Dashboard

- WHATSAPP_TOKEN=EAAQdBJWZCiyk...
- WHATSAPP_PHONE_NUMBER_ID=110735612113186
- WHATSAPP_VERIFY_TOKEN=1285389302894210

## 5. Use Railway URL as Callback URL

Callback URL: https://your-app.railway.app/webhook
Verify Token: 1285389302894210

## Alternative: Heroku (Also Free)

```bash
heroku create whatsapp-medical-bot
heroku config:set WHATSAPP_TOKEN=your_token
heroku config:set WHATSAPP_PHONE_NUMBER_ID=110735612113186
heroku config:set WHATSAPP_VERIFY_TOKEN=1285389302894210
git push heroku main
```

Webhook URL: https://whatsapp-medical-bot.herokuapp.com/webhook

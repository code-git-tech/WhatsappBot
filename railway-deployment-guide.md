# Deploy WhatsApp Bot to Railway (Free)

## Quick Railway Deployment

1. **Sign up at [Railway](https://railway.app)**
2. **Connect your GitHub account**
3. **Push your bot to GitHub:**

   ```bash
   git init
   git add .
   git commit -m "WhatsApp bot"
   git remote add origin https://github.com/yourusername/whatsapp-bot
   git push -u origin main
   ```

4. **Create requirements.txt:**

   ```
   flask==3.0.0
   python-dotenv==1.0.0
   requests==2.31.0
   ```

5. **Create Procfile:**

   ```
   web: python app.py
   ```

6. **Deploy on Railway:**

   - New Project → Deploy from GitHub
   - Select your repository
   - Add environment variables in Railway dashboard:
     - `WHATSAPP_TOKEN`
     - `WHATSAPP_PHONE_NUMBER_ID`
     - `WHATSAPP_VERIFY_TOKEN`
     - `WHATSAPP_NUMBER`
     - `BOT_FLOW_FILE`

7. **Get your Railway URL:** `https://your-app-name.railway.app`

8. **Configure webhook:** `https://your-app-name.railway.app/webhook`

## Alternative: Heroku (Free Tier)

1. **Install Heroku CLI**
2. **Login:** `heroku login`
3. **Create app:** `heroku create your-whatsapp-bot`
4. **Add environment variables:**
   ```bash
   heroku config:set WHATSAPP_TOKEN=your_token
   heroku config:set WHATSAPP_PHONE_NUMBER_ID=110735612113186
   heroku config:set WHATSAPP_VERIFY_TOKEN=1285389302894210
   ```
5. **Deploy:** `git push heroku main`
6. **Webhook URL:** `https://your-whatsapp-bot.herokuapp.com/webhook`

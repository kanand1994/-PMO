# 🚀 Deploy Now - Single URL Deployment

Your Plan My Outings app is ready for **unified deployment** - one URL serves everything!

## ✅ What's Ready

- ✅ Frontend built for production
- ✅ Backend configured to serve frontend
- ✅ Single domain deployment ready
- ✅ No CORS issues
- ✅ All files committed to Git

## 🚀 Deploy in 5 Minutes

### Step 1: Push to GitHub (1 minute)

```bash
# Create repository on GitHub.com first, then:
git remote add origin https://github.com/YOURUSERNAME/plan-my-outings.git
git push -u origin main
```

### Step 2: Deploy to Render (4 minutes)

1. **Go to [Render.com](https://render.com)** → Sign up/Login

2. **New Web Service** → Connect GitHub → Select your repo

3. **Configure:**
   - **Name:** `plan-my-outings`
   - **Root Directory:** `backend`
   - **Build Command:** 
     ```
     cd ../frontend && npm install && npm run build && cd ../backend && pip install -r requirements.txt
     ```
   - **Start Command:** `gunicorn app:app`

4. **Environment Variables:**
   ```
   FLASK_ENV=production
   SECRET_KEY=plan-my-outings-secret-key-2025
   JWT_SECRET_KEY=plan-my-outings-jwt-key-2025
   MAIL_SERVER=smtp.gmail.com
   MAIL_PORT=587
   MAIL_USE_TLS=true
   MAIL_USERNAME=outingplanmy@gmail.com
   MAIL_PASSWORD=ckkymhmweqvrtrfz
   SUPER_ADMIN_USERNAME=superadmin
   SUPER_ADMIN_PASSWORD=SuperAdmin@2025
   SUPER_ADMIN_EMAIL=planmyouting@outlook.com
   SUPER_ADMIN_FIRST_NAME=Super
   SUPER_ADMIN_LAST_NAME=Admin
   ```

5. **Deploy!** → Wait 5-8 minutes

## 🎉 Your Live App

**Single URL serves everything:**
- **Homepage:** `https://your-app.onrender.com`
- **Admin:** `https://your-app.onrender.com/admin`
- **API:** `https://your-app.onrender.com/api/*`

## 🧪 Test Your App

1. Visit your URL
2. Try the contact form (creates user + sends email)
3. Login with generated credentials
4. Access admin dashboard at `/admin`

## 🔐 Admin Login

- **URL:** `https://your-app.onrender.com/admin`
- **Username:** `superadmin`
- **Password:** `SuperAdmin@2025`

---

**That's it!** Your full-stack app is live with one URL! 🌍
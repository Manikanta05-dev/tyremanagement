# Vercel Deployment Guide

## Prerequisites
- GitHub account with your repository
- Vercel account (sign up at https://vercel.com)
- Backend API deployed and accessible

## Step 1: Prepare Your Repository

Your repository is already prepared with:
- ✅ `frontend/vercel.json` configuration
- ✅ Cache-busting enabled
- ✅ Build configuration in `vite.config.js`

## Step 2: Deploy Frontend to Vercel

### Option A: Deploy via Vercel Dashboard (Recommended)

1. **Go to Vercel**
   - Visit https://vercel.com
   - Click "Sign Up" or "Login"
   - Sign in with your GitHub account

2. **Import Your Project**
   - Click "Add New..." → "Project"
   - Select your GitHub repository: `Manikanta05-dev/tyremanagement`
   - Click "Import"

3. **Configure Project Settings**
   ```
   Framework Preset: Vite
   Root Directory: frontend
   Build Command: npm run build
   Output Directory: dist
   Install Command: npm install
   ```

4. **Add Environment Variables**
   Click "Environment Variables" and add:
   ```
   VITE_API_URL=https://your-backend-api-url.com/api
   ```
   Replace with your actual backend URL (Railway, Render, etc.)

5. **Deploy**
   - Click "Deploy"
   - Wait 2-3 minutes for build to complete
   - Your app will be live at: `https://your-project-name.vercel.app`

### Option B: Deploy via Vercel CLI

1. **Install Vercel CLI**
   ```bash
   npm install -g vercel
   ```

2. **Login to Vercel**
   ```bash
   vercel login
   ```

3. **Deploy from Frontend Directory**
   ```bash
   cd frontend
   vercel
   ```

4. **Follow the prompts:**
   - Set up and deploy? `Y`
   - Which scope? Select your account
   - Link to existing project? `N`
   - Project name? `tire-shop-management`
   - Directory? `./` (already in frontend)
   - Override settings? `N`

5. **Set Environment Variables**
   ```bash
   vercel env add VITE_API_URL
   ```
   Enter your backend API URL when prompted

6. **Deploy to Production**
   ```bash
   vercel --prod
   ```

## Step 3: Configure Backend URL

After deployment, update your frontend to use the production backend:

1. **Create `.env.production` in frontend folder:**
   ```env
   VITE_API_URL=https://your-backend-url.com/api
   ```

2. **Redeploy:**
   - Push changes to GitHub (auto-deploys)
   - Or run `vercel --prod` again

## Step 4: Custom Domain (Optional)

1. Go to your Vercel project dashboard
2. Click "Settings" → "Domains"
3. Add your custom domain
4. Follow DNS configuration instructions

## Step 5: Verify Deployment

1. **Open your Vercel URL**
   - Example: `https://tire-shop-management.vercel.app`

2. **Test the following:**
   - ✅ Login page loads with proper styling
   - ✅ Can login successfully
   - ✅ Dashboard loads with data
   - ✅ All pages have correct CSS
   - ✅ Mobile responsive design works
   - ✅ API calls work correctly

## Troubleshooting

### CSS Not Loading
- Clear browser cache (Ctrl + Shift + Delete)
- Check browser console for errors
- Verify `vercel.json` is in frontend folder

### API Connection Issues
- Verify `VITE_API_URL` environment variable
- Check backend CORS settings allow Vercel domain
- Ensure backend is running and accessible

### Build Failures
- Check build logs in Vercel dashboard
- Verify all dependencies in `package.json`
- Ensure Node version compatibility

## Backend CORS Configuration

Update your backend to allow Vercel domain:

```python
# backend/app/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://your-project.vercel.app",  # Add your Vercel URL
        "https://*.vercel.app"  # Allow all Vercel preview deployments
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Automatic Deployments

Vercel automatically deploys:
- **Production**: Every push to `main` branch
- **Preview**: Every pull request and branch push

## Monitoring

- View deployment logs: Vercel Dashboard → Your Project → Deployments
- Check analytics: Vercel Dashboard → Your Project → Analytics
- Monitor performance: Vercel Dashboard → Your Project → Speed Insights

## Cost

- **Free Tier Includes:**
  - Unlimited deployments
  - 100 GB bandwidth/month
  - Automatic HTTPS
  - Global CDN
  - Preview deployments

## Support

- Vercel Docs: https://vercel.com/docs
- Vercel Support: https://vercel.com/support
- Community: https://github.com/vercel/vercel/discussions

---

**Your app is now live on Vercel! 🚀**

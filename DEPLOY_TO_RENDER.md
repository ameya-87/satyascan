# Deploy SatyaScan to Render - Get Your Shareable Link

Follow these steps to deploy SatyaScan and get a permanent shareable link for your CV.

## Step 1: Verify GitHub Repository

Your code should already be on GitHub at: `https://github.com/ameya-87/satyascan`

✅ Make sure all files are committed and pushed:
```bash
git status  # Should show "working tree clean"
```

## Step 2: Sign Up for Render

1. Go to [render.com](https://render.com)
2. Click **"Get Started for Free"** or **"Sign Up"**
3. Sign up with your GitHub account (recommended) or email
4. Verify your email if required

## Step 3: Create a New Web Service

1. Once logged in, click **"New +"** button (top right)
2. Select **"Web Service"**

## Step 4: Connect Your Repository

1. Click **"Connect account"** if you haven't connected GitHub yet
2. Authorize Render to access your GitHub repositories
3. Search for **"satyascan"** or **"multilingual-fake-news"**
4. Click **"Connect"** next to your repository

## Step 5: Configure Your Service

Fill in the following settings:

### Basic Settings:
- **Name**: `satyascan` (or any name you prefer)
- **Region**: Choose closest to you (e.g., "Oregon (US West)")
- **Branch**: `main`
- **Root Directory**: Leave empty (or `.` if needed)

### Build & Deploy Settings:
- **Environment**: `Python 3`
- **Build Command**: 
  ```
  pip install -r requirements.txt
  ```
- **Start Command**: 
  ```
  gunicorn app:app
  ```

### Plan:
- Select **"Free"** plan (perfect for CV projects)

## Step 6: Advanced Settings (Optional but Recommended)

Click **"Advanced"** and add these if needed:

### Environment Variables:
- No environment variables needed for basic setup

### Health Check Path (Optional):
- `/api/health`

## Step 7: Deploy!

1. Click **"Create Web Service"** at the bottom
2. Render will start building your application
3. This takes **5-10 minutes** for the first deployment
4. You'll see build logs in real-time

## Step 8: Get Your Shareable Link

Once deployment completes:

1. You'll see a **green "Live"** status
2. Your URL will be: `https://satyascan.onrender.com` (or your custom name)
3. **This is your shareable link!** ✅

## Step 9: Test Your Deployment

1. Click on your service URL
2. You should see the SatyaScan website
3. Test the analysis feature with sample text
4. Verify all languages are available

## Step 10: Add to Your CV

Add this to your CV/Resume:

```
SatyaScan - AI-Powered News Verification System
🔗 https://satyascan.onrender.com

• Multilingual fake news detection (13+ Indian languages)
• 99% accuracy using Machine Learning
• Real-time analysis with sentiment detection
• Built with Python, Flask, scikit-learn, and Three.js
```

## Important Notes

### Free Tier Limitations:
- **Sleeps after 15 minutes** of inactivity
- First request after sleep takes **30-60 seconds** (wake-up time)
- Perfect for CV/portfolio projects
- Unlimited requests when awake

### Model Files:
- Your model files are already in the `models/` directory
- They'll be included in the deployment
- Total size should be under Render's limits

### Custom Domain (Optional):
- Go to Settings → Custom Domains
- Add your own domain (e.g., `satyascan.com`)
- Follow DNS configuration instructions

## Troubleshooting

### Build Fails:
- Check build logs for errors
- Ensure `requirements.txt` has all dependencies
- Verify `Procfile` exists with: `web: gunicorn app:app`

### Models Not Loading:
- Check that model files are in `models/` directory
- Verify file paths in `app.py` are correct
- Check deployment logs for errors

### Slow First Request:
- Normal on free tier (cold start)
- Subsequent requests are fast
- Consider upgrading for production use

## Updating Your Deployment

When you make changes:

1. Push to GitHub: `git push origin main`
2. Render automatically detects changes
3. Click **"Manual Deploy"** → **"Deploy latest commit"**
4. Wait for deployment to complete

## Your Shareable Link Format

After deployment, your link will be:
```
https://satyascan.onrender.com
```

Or if you chose a different name:
```
https://your-chosen-name.onrender.com
```

---

**🎉 Congratulations!** You now have a permanent, shareable link for SatyaScan that you can add to your CV!


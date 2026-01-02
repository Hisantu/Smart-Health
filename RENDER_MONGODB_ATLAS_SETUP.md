# MongoDB Atlas + Render Deployment Guide

## ✅ Yes, MongoDB Atlas is Perfect for Render!

MongoDB Atlas is an excellent choice for deploying your app on Render. It's:
- ✅ A managed cloud database service (separate from Render)
- ✅ Free tier available (512MB storage)
- ✅ More reliable than Render's free database
- ✅ Industry standard for MongoDB deployments
- ✅ Works seamlessly with Render via connection string

## Setup Steps

### 1. Create MongoDB Atlas Cluster

1. Go to **https://cloud.mongodb.com** and sign up/login
2. Click **"Build a Database"** → Choose **FREE** tier (M0)
3. Choose a cloud provider and region (closest to your users)
4. Click **"Create Cluster"** (takes 1-3 minutes)

### 2. Configure Database Access

1. In MongoDB Atlas dashboard, go to **Database Access**
2. Click **"Add New Database User"**
3. Choose **"Password"** authentication
4. Create username and password (save these!)
5. Under **Database User Privileges**, select **"Read and write to any database"**
6. Click **"Add User"**

### 3. Configure Network Access

1. Go to **Network Access**
2. Click **"Add IP Address"**
3. Click **"Allow Access from Anywhere"** (0.0.0.0/0) - this allows Render to connect
4. Click **"Confirm"**

### 4. Get Connection String

1. Go to **Database** → Click **"Connect"** on your cluster
2. Choose **"Connect your application"**
3. Copy the connection string (looks like):
   ```
   mongodb+srv://<username>:<password>@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
   ```
4. Replace `<username>` and `<password>` with your actual database user credentials
5. Add database name at the end: `/smarthealth?retryWrites=true&w=majority`
   - Final format: `mongodb+srv://username:password@cluster0.xxxxx.mongodb.net/smarthealth?retryWrites=true&w=majority`

### 5. Deploy to Render

#### Option A: Using render.yaml (Recommended)

1. **Push your code to GitHub** (if not already done)
2. Go to **https://render.com** and sign up/login
3. Click **"New +"** → **"Blueprint"**
4. Connect your GitHub repository
5. Render will detect `render.yaml` and deploy automatically
6. **IMPORTANT**: Go to your backend service → **Environment** tab
7. Add environment variable:
   - **Key**: `MONGO_URL`
   - **Value**: Your MongoDB Atlas connection string from step 4
8. Click **"Save Changes"** → Render will redeploy

#### Option B: Manual Setup

1. Go to **https://render.com**
2. **Create Backend Service**:
   - New → Web Service
   - Connect GitHub repo
   - Name: `smart-health-backend`
   - Environment: `Node`
   - Build Command: `cd smart_health/server && npm install`
   - Start Command: `cd smart_health/server && npm start`
   - Add Environment Variables:
     - `NODE_ENV` = `production`
     - `PORT` = `10000`
     - `MONGO_URL` = `mongodb+srv://username:password@cluster0.xxxxx.mongodb.net/smarthealth?retryWrites=true&w=majority`
     - `JWT_SECRET` = (generate a random string)
3. **Create Frontend Service**:
   - New → Static Site
   - Connect GitHub repo
   - Name: `smart-health-frontend`
   - Build Command: `cd smart_health/web && npm install && npm run build`
   - Publish Directory: `smart_health/web/dist`
   - Add Environment Variable:
     - `VITE_API_URL` = `https://smart-health-backend.onrender.com/api`

### 6. Initialize Database (After Deployment)

1. In Render dashboard, go to your backend service
2. Click **"Shell"** tab
3. Run: `cd smart_health/server && npm run seed`
4. This will create initial users (admin/admin123)

### 7. Test Your Deployment

- Frontend: `https://smart-health-frontend.onrender.com`
- Backend API: `https://smart-health-backend.onrender.com/api`
- Test Login: `admin` / `admin123`

## Important Notes

⚠️ **Security**: Never commit your MongoDB Atlas connection string to GitHub
✅ The `MONGO_URL` is set in Render Dashboard (not in code)
✅ MongoDB Atlas free tier includes 512MB storage - perfect for small apps
✅ Your database runs separately from Render, so it persists even if you change hosting

## Troubleshooting

- **Connection Failed**: Check that Network Access allows 0.0.0.0/0
- **Authentication Failed**: Verify username/password in connection string
- **Database Not Found**: Make sure database name is in connection string (`/smarthealth`)
- **Build Fails**: Check Render build logs for errors


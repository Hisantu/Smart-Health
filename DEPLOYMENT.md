# Smart Health System - Deployment Guide

## GitHub Push Instructions

1. **Initialize Git Repository**
```bash
cd E:\smart_health
git init
git add .
git commit -m "Initial commit: Smart Health Queue Management System"
```

2. **Add Remote Repository**
```bash
git remote add origin https://github.com/Prajwal719/smart_health-.git
git branch -M main
git push -u origin main
```

## Render Deployment Instructions

### Option 1: Using Render Dashboard (Recommended)

1. **Go to Render Dashboard**: https://render.com
2. **Create New Web Service** for Backend:
   - Repository: `https://github.com/Prajwal719/smart_health-.git`
   - Name: `smart-health-backend`
   - Environment: `Node`
   - Build Command: `cd smart_health/server && npm install`
   - Start Command: `cd smart_health/server && npm start`
   - Add Environment Variables:
     - `NODE_ENV=production`
     - `PORT=10000`
     - `JWT_SECRET=your_jwt_secret_here_change_me_production`
     - `MONGO_URL=mongodb+srv://username:password@cluster.mongodb.net/smarthealth`

3. **Create New Static Site** for Frontend:
   - Repository: `https://github.com/Prajwal719/smart_health-.git`
   - Name: `smart-health-frontend`
   - Build Command: `cd smart_health/web && npm install && npm run build`
   - Publish Directory: `smart_health/web/dist`
   - Add Environment Variable:
     - `VITE_API_URL=https://smart-health-backend.onrender.com/api`

4. **Create MongoDB Database**:
   - Use MongoDB Atlas (free tier)
   - Get connection string
   - Update MONGO_URL in backend service

### Option 2: Using render.yaml (Alternative)

1. Push the `render.yaml` file to your repository
2. Connect repository to Render
3. Render will automatically deploy based on the configuration

## Environment Variables Setup

### Backend (.env for local development)
```
PORT=4000
MONGO_URL=mongodb://localhost:27017/smarthealth
JWT_SECRET=your_jwt_secret_here_change_me
TWILIO_ACCOUNT_SID=
TWILIO_AUTH_TOKEN=
TWILIO_FROM=
```

### Frontend (.env for local development)
```
VITE_API_URL=http://localhost:4000/api
```

## MongoDB Atlas Setup (for Production)

1. Go to https://cloud.mongodb.com
2. Create free cluster
3. Create database user
4. Whitelist IP addresses (0.0.0.0/0 for all)
5. Get connection string
6. Replace in MONGO_URL environment variable

## Post-Deployment Steps

1. **Seed Database** (run once):
   - Access backend service terminal in Render
   - Run: `npm run seed`

2. **Test Application**:
   - Frontend URL: `https://smart-health-frontend.onrender.com`
   - Backend URL: `https://smart-health-backend.onrender.com`
   - Test login with: admin/admin123

## Troubleshooting

- **Build Fails**: Check build logs in Render dashboard
- **Database Connection**: Verify MongoDB Atlas connection string
- **CORS Issues**: Backend already configured for production
- **Socket.io**: Uses same domain as API, should work automatically

## Default Login Credentials
- Admin: `admin` / `admin123`
- Receptionist: `receptionist` / `recep123`
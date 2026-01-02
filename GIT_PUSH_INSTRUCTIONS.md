# Instructions to Push Project to GitHub

## Your Repository: https://github.com/Hisantu/Smart-Health

### Step-by-Step Commands (Run these in PowerShell from D:\smart_health)

```powershell
# Navigate to project root
cd D:\smart_health

# Initialize git repository (if not already initialized)
git init

# Remove submodule entry if it exists
git rm --cached smart_health 2>$null

# Add remote (remove old one first if exists)
git remote remove origin 2>$null
git remote add origin https://github.com/Hisantu/Smart-Health.git

# Add all files
git add .

# Commit
git commit -m "Complete Smart Health project: frontend and backend with MongoDB Atlas setup"

# Push to GitHub (force push if needed since remote might have old commits)
git push -u origin main
```

### If push fails, use force push:
```powershell
git push -f origin main
```

### Important Notes:
- ✅ The nested .git directory has been removed from smart_health/smart_health
- ✅ Your MongoDB Atlas connection string is saved in `MONGO_URL_FOR_RENDER.txt` (DO NOT commit this - it's in .gitignore)
- ✅ The render.yaml is configured to use MongoDB Atlas
- ✅ All frontend and backend code will be pushed

### After Pushing:
1. Go to Render Dashboard
2. Connect your GitHub repository (https://github.com/Hisantu/Smart-Health)
3. Render will detect render.yaml and deploy automatically
4. Add MONGO_URL environment variable in Render Dashboard with your MongoDB Atlas connection string


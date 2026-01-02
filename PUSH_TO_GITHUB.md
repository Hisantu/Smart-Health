# Instructions to Push Project to GitHub

## Steps to Fix and Push

You have a nested git repository issue. Follow these steps in PowerShell:

### Step 1: Remove nested .git directory (if exists)
```powershell
cd D:\smart_health
if (Test-Path "smart_health\.git") { Remove-Item -Recurse -Force "smart_health\.git" }
```

### Step 2: Remove submodule entry from git
```powershell
git rm --cached smart_health
```

### Step 3: Update remote URL to correct repository
```powershell
git remote set-url origin https://github.com/Hisantu/Smart-Health.git
```

### Step 4: Add all files
```powershell
git add .
```

### Step 5: Commit
```powershell
git commit -m "Complete project: frontend and backend"
```

### Step 6: Push to GitHub
```powershell
git push -u origin main
```

## If git push fails, force push (use carefully):
```powershell
git push -f origin main
```


# Script to fix nested git repository and push to GitHub
Write-Host "=== Fixing Git Repository and Pushing to GitHub ===" -ForegroundColor Cyan

# Step 1: Navigate to project root
Set-Location D:\smart_health
Write-Host "`n[1/7] Current directory: $(Get-Location)" -ForegroundColor Yellow

# Step 2: Remove nested .git directory if it exists
Write-Host "`n[2/7] Checking for nested .git directory..." -ForegroundColor Yellow
if (Test-Path "smart_health\.git") {
    Write-Host "Found nested .git directory, removing it..." -ForegroundColor Red
    Remove-Item -Recurse -Force "smart_health\.git"
    Write-Host "Nested .git removed!" -ForegroundColor Green
} else {
    Write-Host "No nested .git found" -ForegroundColor Green
}

# Step 3: Remove submodule entry if it exists
Write-Host "`n[3/7] Removing submodule entry from git..." -ForegroundColor Yellow
git rm --cached smart_health 2>$null
Write-Host "Submodule entry removed (if it existed)" -ForegroundColor Green

# Step 4: Update remote URL
Write-Host "`n[4/7] Updating remote URL to https://github.com/Hisantu/Smart-Health.git..." -ForegroundColor Yellow
git remote remove origin 2>$null
git remote add origin https://github.com/Hisantu/Smart-Health.git
Write-Host "Remote URL updated!" -ForegroundColor Green

# Step 5: Add all files
Write-Host "`n[5/7] Adding all files to git..." -ForegroundColor Yellow
git add .
Write-Host "All files added!" -ForegroundColor Green

# Step 6: Commit
Write-Host "`n[6/7] Committing changes..." -ForegroundColor Yellow
git commit -m "Complete Smart Health project: frontend and backend"
Write-Host "Changes committed!" -ForegroundColor Green

# Step 7: Push to GitHub
Write-Host "`n[7/7] Pushing to GitHub..." -ForegroundColor Yellow
Write-Host "Pushing to https://github.com/Hisantu/Smart-Health.git" -ForegroundColor Cyan
git push -u origin main

Write-Host "`n=== Done! ===" -ForegroundColor Green
Write-Host "If push failed, you may need to force push with: git push -f origin main" -ForegroundColor Yellow


# PowerShell script to add Python and uv to user PATH
Write-Host "Setting up PATH for Python and uv..." -ForegroundColor Cyan

$pythonPath = "C:\Users\SRETH\AppData\Local\Programs\Python\Python314"
$uvPath = "C:\Users\SRETH\AppData\Local\Programs\Python\Python314\Scripts"
$gitPath = "C:\Users\SRETH\AppData\Local\Programs\Git\bin"
$popplerPath = "C:\Users\SRETH\AppData\Local\Programs\poppler\poppler-25.12.0\Library\bin"

# Verify paths exist
if (Test-Path $pythonPath) {
    Write-Host "? Python directory found: $pythonPath" -ForegroundColor Green
} else {
    Write-Host "? Python directory not found: $pythonPath" -ForegroundColor Red
}

if (Test-Path $uvPath) {
    Write-Host "? Scripts directory found: $uvPath" -ForegroundColor Green
} else {
    Write-Host "? Scripts directory not found: $uvPath" -ForegroundColor Red
}

if (Test-Path $gitPath) {
    Write-Host "? Git directory found: $gitPath" -ForegroundColor Green
} else {
    Write-Host "? Git directory not found: $gitPath" -ForegroundColor Red
}

if (Test-Path $popplerPath) {
    Write-Host "? Poppler directory found: $popplerPath" -ForegroundColor Green
} else {
    Write-Host "? Poppler directory not found: $popplerPath" -ForegroundColor Red
}

# Get current user PATH
$currentPath = [Environment]::GetEnvironmentVariable("Path", "User")

# Check if paths are already in PATH (exact match to avoid false positives)
$pathsToAdd = @()
$currentPathArray = $currentPath -split ';'

if ($currentPathArray -notcontains $pythonPath) {
    $pathsToAdd += $pythonPath
    Write-Host "Adding Python to PATH..." -ForegroundColor Yellow
} else {
    Write-Host "Python path already in PATH" -ForegroundColor Gray
}

if ($currentPathArray -notcontains $uvPath) {
    $pathsToAdd += $uvPath
    Write-Host "Adding Scripts (uv) to PATH..." -ForegroundColor Yellow
} else {
    Write-Host "Scripts path already in PATH" -ForegroundColor Gray
}

if ($currentPathArray -notcontains $gitPath) {
    $pathsToAdd += $gitPath
    Write-Host "Adding Git to PATH..." -ForegroundColor Yellow
} else {
    Write-Host "Git path already in PATH" -ForegroundColor Gray
}

if ($currentPathArray -notcontains $popplerPath) {
    $pathsToAdd += $popplerPath
    Write-Host "Adding Poppler to PATH..." -ForegroundColor Yellow
} else {
    Write-Host "Poppler path already in PATH" -ForegroundColor Gray
}

# Add paths if needed
if ($pathsToAdd.Count -gt 0) {
    $newPath = $currentPath
    foreach ($path in $pathsToAdd) {
        $newPath += ";$path"
    }
    
    [Environment]::SetEnvironmentVariable("Path", $newPath, "User")
    Write-Host "`n? PATH updated successfully!" -ForegroundColor Green
    Write-Host "`nIMPORTANT: Close and restart your terminal/Command Prompt for changes to take effect." -ForegroundColor Yellow
} else {
    Write-Host "`nNo changes needed - paths already configured." -ForegroundColor Green
}

# Show current user PATH
Write-Host "`nCurrent User PATH:" -ForegroundColor Cyan
[Environment]::GetEnvironmentVariable("Path", "User") -split ';' | ForEach-Object { Write-Host "  $_" }
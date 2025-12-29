# PowerShell Profile Configuration for Virtual Environment Prompt
# This script customizes your PowerShell prompt to show the virtual environment name

# Function to customize the prompt
function prompt {
    # Get the current virtual environment
    $venvPrompt = ""
    if ($env:VIRTUAL_ENV) {
        $venvName = Split-Path $env:VIRTUAL_ENV -Leaf
        $venvPrompt = "($venvName) "
    }
    
    # Get current location
    $currentPath = $executionContext.SessionState.Path.CurrentLocation.Path
    
    # Build the prompt
    Write-Host $venvPrompt -NoNewline -ForegroundColor Green
    Write-Host $currentPath -NoNewline -ForegroundColor Cyan
    return "> "
}

Write-Host "PowerShell prompt customization loaded!" -ForegroundColor Yellow
Write-Host "Virtual environment name will be shown in green when activated." -ForegroundColor Yellow

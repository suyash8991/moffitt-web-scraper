# Save this as fix_python_path.ps1 and run it in PowerShell
# This will put Miniconda Python first in your PATH

# Prepend Miniconda paths to PATH
$env:PATH = "C:\Users\suyas\miniconda3;C:\Users\suyas\miniconda3\Scripts;C:\Users\suyas\miniconda3\Library\bin;" + $env:PATH

# Create a function to set Python alias
function Set-CondaPython {
    Set-Alias -Name python -Value "C:\Users\suyas\miniconda3\python.exe" -Scope Global -Force
    Set-Alias -Name pip -Value "C:\Users\suyas\miniconda3\Scripts\pip.exe" -Scope Global -Force
    Write-Host "Python and pip aliases set to Miniconda versions"
}

# Run the function
Set-CondaPython

# Show the current Python path
Write-Host "Current Python: $(where.exe python | Select-Object -First 1)"

# Test if pip works
try {
    $pipVersion = python -m pip --version
    Write-Host "Pip is working: $pipVersion"
} catch {
    Write-Host "Error running pip: $_"
}

# Instructions for making this permanent
Write-Host "`nTo make these changes permanent, add this script to your PowerShell profile:`n"
Write-Host "1. Edit your profile: notepad $PROFILE"
Write-Host "2. Add this line: . 'C:\path\to\fix_python_path.ps1'"
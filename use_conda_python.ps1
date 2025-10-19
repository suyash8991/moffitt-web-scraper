# Simple script to force using the Miniconda Python for a specific script with arguments
# Usage: .\use_conda_python.ps1 .\main.py --arg1 value1 --arg2 value2

# Path to Miniconda Python
$pythonPath = "C:\Users\suyas\miniconda3\python.exe"

# Get all arguments passed to this script
$scriptArgs = $args

if ($scriptArgs.Count -eq 0) {
    Write-Host "Error: No script specified to run."
    Write-Host "Usage: .\use_conda_python.ps1 [script.py] [arguments...]"
    exit 1
}

# First argument is the Python script to run
$scriptToRun = $scriptArgs[0]
$scriptArgs = $scriptArgs[1..$scriptArgs.Length]

# Build the command with proper argument handling
$argumentString = ""
foreach ($arg in $scriptArgs) {
    # Check if argument contains spaces, if so, add quotes
    if ($arg -match "\s") {
        $argumentString += " `"$arg`""
    } else {
        $argumentString += " $arg"
    }
}

# Run the command using the full path to Python
$fullCommand = "& `"$pythonPath`" `"$scriptToRun`"$argumentString"
Write-Host "Running: $fullCommand"

# Execute the command
Invoke-Expression $fullCommand
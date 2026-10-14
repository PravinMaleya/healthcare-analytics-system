
$ErrorActionPreference = "Stop"

$ProjectRoot = "C:\Users\Prof\Desktop\Projects\healthcare-analytics-system"
$LogDir = Join-Path $ProjectRoot "logs"

New-Item -ItemType Directory -Path $LogDir -Force | Out-Null

$Timestamp = Get-Date -Format "yyyy-MM-dd_HH-mm-ss"
$LogFile = Join-Path $LogDir "retraining_$Timestamp.log"

Set-Location $ProjectRoot

"Retraining started: $(Get-Date)" | Out-File $LogFile

& "C:\Users\Prof\.local\bin\uv.exe" run --locked python -m ml.train *>> $LogFile

if ($LASTEXITCODE -eq 0) {
    "Retraining completed successfully: $(Get-Date)" | Out-File $LogFile -Append
} else {
    "Retraining failed with exit code $LASTEXITCODE at $(Get-Date)" | Out-File $LogFile -Append
    exit $LASTEXITCODE
}

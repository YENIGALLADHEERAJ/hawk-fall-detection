param([string]$Python = 'python')
$ErrorActionPreference = 'Stop'
$repo = Split-Path $PSScriptRoot -Parent
Push-Location $repo
try {
    & $Python -m pip --version
    if ($LASTEXITCODE -ne 0) { throw 'Choose a working Python 3.12 with pip using -Python.' }
    if (-not (Test-Path '.venv/Scripts/python.exe')) {
        & $Python -m venv --without-pip .venv
        if ($LASTEXITCODE -ne 0) { throw 'Virtual environment creation failed.' }
    }
    & $Python -m pip --python '.venv/Scripts/python.exe' install -r requirements-vision.txt
    if ($LASTEXITCODE -ne 0) { throw 'Dependency installation failed.' }
    & '.venv/Scripts/python.exe' scripts/verify_environment.py
    if ($LASTEXITCODE -ne 0) { throw 'OpenCV 5 verification failed.' }
} finally { Pop-Location }

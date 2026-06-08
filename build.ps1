$ErrorActionPreference = "Stop"

python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install pyinstaller

pyinstaller `
  --noconsole `
  --onefile `
  --name TopNote `
  --clean `
  main.py

Write-Host ""
Write-Host "Build complete: dist\TopNote.exe"

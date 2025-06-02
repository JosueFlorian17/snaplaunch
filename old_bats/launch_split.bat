@echo off
set NIRCMD_PATH="C:\Users\Florian\Downloads\snaplauncher\nir\nircmd.exe"
set CHROME_PATH="C:\Program Files\Google\Chrome\Application\chrome.exe"

start "" "C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE"
timeout /t 2 >nul
%NIRCMD_PATH% win move ititle "Word" 0 0 960 1080
start "" "C:\xampp\xampp-control.exe"
timeout /t 2 >nul
%NIRCMD_PATH% win move ititle "XAMPP Control Panel" 960 0 960 1080
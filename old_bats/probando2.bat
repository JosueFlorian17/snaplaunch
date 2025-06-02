@echo off
REM Ruta de Chrome
set CHROME_PATH="C:\Program Files\Google\Chrome\Application\chrome.exe"

set NIRCMD_PATH="C:\Users\Florian\Downloads\snaplauncher\nir\nircmd.exe"

REM Abrir en modo app
start "" %CHROME_PATH% --app=https://web.whatsapp.com/
timeout /t 2 >nul
start "" %CHROME_PATH% --app=https://www.youtube.com/
timeout /t 2 >nul
start "" %CHROME_PATH% --app=https://mail.google.com/mail/u/0/#inbox
timeout /t 2 >nul
start "" %CHROME_PATH% --app=https://x.com/home
timeout /t 2 >nul
start "" %CHROME_PATH% --app=https://calendar.google.com/calendar/u/0/r?pli=1

timeout /t 6 >nul



REM Grupo 1: WhatsApp y YouTube
%NIRCMD_PATH% win move ititle "web.whatsapp.com" 0 0 
%NIRCMD_PATH% win move ititle "YouTube" 960 0 
timeout /t 1 >nul

REM Grupo 2: Gmail y X
%NIRCMD_PATH% win move ititle "Recibidos" 0 0 
%NIRCMD_PATH% win move ititle "Inicio / X" 960 0 
timeout /t 1 >nul

REM Grupo 3: Calendar (izquierda) — derecha queda vacía
%NIRCMD_PATH% win move ititle "Calendario de Google" 0 0 

@echo off
set CHROME="C:\Program Files\Google\Chrome\Application\chrome.exe"
set NIRCMD="C:\Users\Florian\Downloads\snaplauncher\nir\nircmd.exe"

start "" %CHROME% --new-window https://www.google.com
timeout /t 2 >nul
start "" %CHROME% --new-window https://www.youtube.com
timeout /t 3 >nul

rem Asumimos pantalla 1920x1080. Ajusta si es necesario.
%NIRCMD% win move title "Google Chrome" 0 0 960 1080
%NIRCMD% win move title "Google Chrome" 960 0 960 1080

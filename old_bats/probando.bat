@echo off
REM Ruta de Chrome
set CHROME_PATH="C:\Program Files\Google\Chrome\Application\chrome.exe"

REM Ruta de NirCmd (ajusta si está en otra carpeta)
set NIRCMD_PATH="C:\Users\Florian\Downloads\snaplauncher\nir\nircmd.exe"

REM Abrir URLs en modo app (ventanas independientes)
start "" %CHROME_PATH%  --new-window https://web.whatsapp.com/
timeout /t 2 >nul
start "" %CHROME_PATH% --new-window https://www.youtube.com/
timeout /t 2 >nul
start "" %CHROME_PATH% --new-window https://mail.google.com/mail/u/0/#inbox
timeout /t 2 >nul
start "" %CHROME_PATH% --new-window https://x.com/home
timeout /t 2 >nul
start "" %CHROME_PATH% --new-window https://calendar.google.com/calendar/u/0/r?pli=1

REM Esperar que se abran todas las ventanas
timeout /t 5 >nul

REM Definir resolución y tamaño (ajusta a tu pantalla)
set WIDTH=1920
set HEIGHT=1080
set PART_WIDTH=384 REM 1920 / 5 = 384 pixeles ancho por ventana

REM Mover y redimensionar ventanas por título parcial (dominio)
%NIRCMD_PATH% win move ititle "web.whatsapp.com" 0 0 %PART_WIDTH% %HEIGHT%
%NIRCMD_PATH% win move ititle "youtube.com" %PART_WIDTH% 0 %PART_WIDTH% %HEIGHT%
%NIRCMD_PATH% win move ititle "mail.google.com" %PART_WIDTH%*2 0 %PART_WIDTH% %HEIGHT%
%NIRCMD_PATH% win move ititle "x.com" %PART_WIDTH%*3 0 %PART_WIDTH% %HEIGHT%
%NIRCMD_PATH% win move ititle "calendar.google.com" %PART_WIDTH%*4 0 %PART_WIDTH% %HEIGHT%

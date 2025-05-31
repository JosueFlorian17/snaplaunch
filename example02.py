import subprocess
import time
from pywinauto import Desktop
import pyautogui

# Abrir dos ventanas nuevas de Chrome con YouTube
subprocess.Popen(['start', 'chrome', '--new-window', 'https://www.youtube.com'], shell=True)
subprocess.Popen(['start', 'chrome', '--new-window', 'https://www.youtube.com'], shell=True)

max_wait = 10  # segundos
waited = 0
interval = 0.5

desktop = Desktop(backend="win32")
chrome_windows = []

# Esperar hasta encontrar 2 ventanas o hasta timeout
while waited < max_wait:
    chrome_windows = [w for w in desktop.windows() if 'YouTube' in w.window_text()]
    if len(chrome_windows) >= 2:
        break
    time.sleep(interval)
    waited += interval

if len(chrome_windows) < 2:
    print("No se encontraron dos ventanas de YouTube abiertas después de esperar.")
    exit()

screen_width, screen_height = pyautogui.size()

win1 = chrome_windows[0]
win2 = chrome_windows[1]

# Mover y redimensionar ventanas
win1.move_window(0, 0, screen_width // 2, screen_height, repaint=True)
win2.move_window(screen_width // 2, 0, screen_width // 2, screen_height, repaint=True)

import subprocess
import time
from pywinauto import Desktop
import pyautogui

# Abrir dos ventanas nuevas de Chrome con YouTube
subprocess.Popen(['start', 'chrome', '--new-window', 'https://www.youtube.com'], shell=True)
subprocess.Popen(['start', 'chrome', '--new-window', 'https://www.youtube.com'], shell=True)

time.sleep(1)  # Esperar que abran

screen_width, screen_height = pyautogui.size()

desktop = Desktop(backend="win32")  # Cambiado a win32

# Buscar ventanas de Chrome que contengan YouTube en el título
chrome_windows = [w for w in desktop.windows() if 'YouTube' in w.window_text()]

if len(chrome_windows) < 2:
    print("No se encontraron dos ventanas de YouTube abiertas.")
    exit()

win1 = chrome_windows[0]
win2 = chrome_windows[1]

# Usar move_window para mover y redimensionar
win1.move_window(0, 0, screen_width // 2, screen_height, repaint=True)
win2.move_window(screen_width // 2, 0, screen_width // 2, screen_height, repaint=True)

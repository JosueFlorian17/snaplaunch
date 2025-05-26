import subprocess
import time
import pyautogui

# Ruta de Chrome y NirCmd
chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
nircmd_path = r"C:\Users\Florian\Downloads\snaplauncher\nir\nircmd.exe"  # ← Reemplaza con la ruta real

# URLs a abrir
urls = ["https://www.google.com", "https://www.youtube.com"]

# Abrir ventanas
subprocess.Popen([chrome_path, "--new-window", urls[0]])
time.sleep(1.5)
subprocess.Popen([chrome_path, "--new-window", urls[1]])
time.sleep(3)

# Obtener resolución
screen_width, screen_height = pyautogui.size()
half_width = screen_width // 2

# Mover y redimensionar ventanas con NirCmd
# Nota: Esto moverá las 2 últimas ventanas de Chrome
subprocess.run([nircmd_path, "win", "move", "ititle", "Google Chrome", "0", "0", str(half_width), str(screen_height)])
subprocess.run([nircmd_path, "win", "move", "ititle", "Google Chrome", str(half_width), "0", str(half_width), str(screen_height)])

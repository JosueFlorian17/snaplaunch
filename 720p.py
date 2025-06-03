import subprocess
import time
import re
import pygetwindow as gw

# Lista de aplicaciones adaptadas a resolución 1280x720
apps = [
    {
        'command': r"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE",
        'pattern': r'word',
        'position': (0, 0, 640, 305),  # top-left
    },
    {
        'command': r"C:\xampp\xampp-control.exe",
        'pattern': r'xampp\ control\ panel',
        'position': (633, 0, 653, 365),  # top-right
    },
    {
        'command': r"C:\Windows\system32\mspaint.exe",
        'pattern': r'paint',
        'position': (-5, 358, 649, 365),  # bottom-left
    },
    {
        'command': r"C:\Windows\system32\mspaint.exe",
        'pattern': r'paint',
        'position': (633, 358, 653, 365),  # bottom-right
    },
]

def launch_and_position(app):
    print(f"Lanzando: {app['command']}")
    subprocess.Popen(app['command'], shell=True)
    time.sleep(3)
    window = None
    for w in gw.getAllWindows():
        if re.search(app['pattern'], w.title, re.IGNORECASE):
            window = w
            break
    if window:
        x, y, w_, h_ = app['position']
        try:
            window.moveTo(x, y)
            window.resizeTo(w_, h_)
            print(f"✔ Posicionada: {window.title}")
        except Exception as e:
            print(f"⚠ No se pudo mover: {e}")
    else:
        print(f"❌ No se encontró ventana que coincida con el patrón: {app['pattern']}")

for app in apps:
    launch_and_position(app)

print('✅ Todas las apps fueron abiertas y posicionadas.')

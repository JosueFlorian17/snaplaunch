import os
import win32com.client
from pathlib import Path

# Rutas al menú inicio del sistema y del usuario
START_MENU_PATHS = [
    os.getenv("APPDATA") + r"\Microsoft\Windows\Start Menu\Programs",
    os.getenv("PROGRAMDATA") + r"\Microsoft\Windows\Start Menu\Programs"
]

# Palabras clave para excluir (más robusto)
EXCLUDE_KEYWORDS = [
    'python', 'idle', 'Uninstall', 'documentation', 'update', 'readme',
    'java', 'node', 'vscode', 'git', 'maintenance', 'help', 'manual',
    'diagnostic', 'debug', 'repair', 'support', 'tool', 'setup', 'install',
    "desinstalar", "desinstalador", "desinstalación", "uninstaller", "unins"
]

def get_shortcut_target(path):
    """Devuelve la ruta real del .lnk (acceso directo)"""
    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortCut(str(path))
    return shortcut.Targetpath

def is_common_app(path):
    """Verifica que el destino sea una app de usuario común"""
    if not path.lower().endswith('.exe'):
        return False
    path_lower = path.lower()
    return not any(keyword in path_lower for keyword in EXCLUDE_KEYWORDS)

def find_installed_apps():
    apps = {}

    for start_path in START_MENU_PATHS:
        for root, _, files in os.walk(start_path):
            for file in files:
                if file.endswith(".lnk"):
                    full_path = Path(root) / file
                    try:
                        target = get_shortcut_target(full_path)
                        if is_common_app(target):
                            app_name = file.replace('.lnk', '').strip()
                            apps[app_name] = target
                    except Exception:
                        continue

    return apps

if __name__ == "__main__":
    apps = find_installed_apps()
    print("Aplicaciones instaladas comunes encontradas:\n")
    for name, path in sorted(apps.items()):
        print(f"{name} -> {path}")

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

BROWSERS = ["chrome", "brave", "edge"]

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

def ask_user_selection(app_list):
    print("\nAplicaciones encontradas:\n")
    for i, (name, path) in enumerate(app_list):
        print(f"{i+1}. {name} -> {path}")

    selected = input("\nIngresa los números de las apps que deseas abrir (separados por comas): ")
    indices = [int(x.strip()) - 1 for x in selected.split(",") if x.strip().isdigit()]
    return [app_list[i] for i in indices if 0 <= i < len(app_list)]

def get_browser_urls():
    urls = []
    print("Has elegido un navegador. Ingresa las URLs que quieres abrir (una por línea).")
    print("Presiona Enter sin escribir nada para terminar.")
    while True:
        url = input("URL: ").strip()
        if not url:
            break
        urls.append(url)
    return urls

def generate_bat(selected_apps, chrome_path, nircmd_path, output_path="launch_apps.bat"):
    lines = ['@echo off']
    lines.append(f'REM Ruta de Chrome\nset CHROME_PATH="{chrome_path}"')
    lines.append(f'set NIRCMD_PATH="{nircmd_path}"\n')

    window_index = 0
    browser_count = 0

    for name, path in selected_apps:
        exe_lower = path.lower()
        if any(browser in exe_lower for browser in BROWSERS):
            urls = get_browser_urls()
            for url in urls:
                lines.append(f'start "" %CHROME_PATH% --app={url}')
                lines.append('timeout /t 2 >nul')
                window_title = url.split("//")[-1].split("/")[0]
                lines.append(f'%NIRCMD_PATH% win move ititle "{window_title}" {960 * (window_index % 2)} 0')
                if window_index % 2 == 1:
                    lines.append('timeout /t 1 >nul')
                window_index += 1
            browser_count += 1
        else:
            lines.append(f'start "" "{path}"')

    if browser_count > 0:
        lines.append('\ntimeout /t 6 >nul')

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"\nArchivo BAT generado exitosamente: {output_path}")

if __name__ == "__main__":
    apps = find_installed_apps()
    sorted_apps = sorted(apps.items())
    selected = ask_user_selection(sorted_apps)

    # Puedes personalizar estas rutas
    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    nircmd_path = r"C:\Users\Florian\Downloads\snaplauncher\nir\nircmd.exe"

    generate_bat(selected, chrome_path, nircmd_path)

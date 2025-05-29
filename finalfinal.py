import os
import win32com.client
from pathlib import Path
import tkinter

START_MENU_PATHS = [
    os.getenv("APPDATA") + r"\Microsoft\Windows\Start Menu\Programs",
    os.getenv("PROGRAMDATA") + r"\Microsoft\Windows\Start Menu\Programs"
]

EXCLUDE_KEYWORDS = [
    'python', 'idle', 'Uninstall', 'documentation', 'update', 'readme',
    'java', 'node', 'vscode', 'git', 'maintenance', 'help', 'manual',
    'diagnostic', 'debug', 'repair', 'support', 'tool', 'setup', 'install',
    "desinstalar", "desinstalador", "desinstalación", "uninstaller", "unins"
]

BROWSERS = ["chrome", "brave", "edge"]

def get_shortcut_target(path):
    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortCut(str(path))
    return shortcut.Targetpath

def is_common_app(path):
    if not path.lower().endswith('.exe'):
        return False
    return not any(keyword in path.lower() for keyword in EXCLUDE_KEYWORDS)

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
    print("\nHas elegido un navegador. Ingresa las URLs que quieres abrir (una por línea).")
    print("Presiona Enter sin escribir nada para terminar.")
    while True:
        url = input("URL: ").strip()
        if not url:
            break
        urls.append(url)
    return urls

def get_screen_resolution():
    root = tkinter.Tk()
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    root.destroy()
    return width, height

def display_layout_options():
    print("\nModos de pantalla dividida:")
    print("1. Vertical Doble → 2 apps lado a lado")
    print("2. Cuadrantes (2x2) → 4 apps")
    print("3. Principal Izquierda + 2 Derechas apiladas")
    print("4. 2 Izquierdas + Principal Derecha")
    print("5. Horizontal Doble → 2 apps una encima de otra")

def get_layout_positions(choice, width, height):
    positions = []
    if choice == '1':
        w = width // 2
        positions = [(0, 0, w, height), (w, 0, w, height)]
    elif choice == '2':
        w, h = width // 2, height // 2
        positions = [(0, 0, w, h), (w, 0, w, h), (0, h, w, h), (w, h, w, h)]
    elif choice == '3':
        main_w = int(width * 0.66)
        side_w = width - main_w
        side_h = height // 2
        positions = [(0, 0, main_w, height), (main_w, 0, side_w, side_h), (main_w, side_h, side_w, side_h)]
    elif choice == '4':
        main_w = int(width * 0.66)
        side_w = width - main_w
        side_h = height // 2
        positions = [(0, 0, side_w, side_h), (0, side_h, side_w, side_h), (side_w, 0, main_w, height)]
    elif choice == '5':
        h = height // 2
        positions = [(0, 0, width, h), (0, h, width, h)]
    return positions

def assign_apps_to_positions(apps, positions):
    assignments = []
    for i, pos in enumerate(positions):
        print(f"\nPosición {i+1} (x={pos[0]}, y={pos[1]}, w={pos[2]}, h={pos[3]})")
        for j, (name, _) in enumerate(apps):
            print(f"  {j+1}. {name}")
        choice = int(input("¿Qué app va aquí? (ingresa el número): ")) - 1
        assignments.append((apps[choice], pos))
    return assignments

def generate_bat(assignments, chrome_path, nircmd_path, output_path="launch_split.bat"):
    lines = ['@echo off']
    lines.append(f'set NIRCMD_PATH="{nircmd_path}"')
    lines.append(f'set CHROME_PATH="{chrome_path}"')
    lines.append('')

    for (name, path), (x, y, w, h) in assignments:
        exe_lower = path.lower()
        if any(browser in exe_lower for browser in BROWSERS):
            urls = get_browser_urls()
            for url in urls:
                lines.append(f'start "" %CHROME_PATH% --app={url}')
                window_title = url.split("//")[-1].split("/")[0]
                lines.append(f'timeout /t 2 >nul')
                lines.append(f'%NIRCMD_PATH% win move ititle "{window_title}" {x} {y} {w} {h}')
        else:
            lines.append(f'start "" "{path}"')
            lines.append(f'timeout /t 2 >nul')
            lines.append(f'%NIRCMD_PATH% win move ititle "{name}" {x} {y} {w} {h}')

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"\nArchivo BAT generado exitosamente: {output_path}")

# ------------------------------
# EJECUCIÓN PRINCIPAL
# ------------------------------
if __name__ == "__main__":
    apps = find_installed_apps()
    sorted_apps = sorted(apps.items())
    selected = ask_user_selection(sorted_apps)

    use_split = input("\n¿Deseas usar pantalla dividida? (s/n): ").strip().lower() == 's'
    if use_split:
        screen_w, screen_h = get_screen_resolution()
        display_layout_options()
        layout_choice = input("Elige el número del modo de pantalla dividida: ").strip()
        positions = get_layout_positions(layout_choice, screen_w, screen_h)
        assignments = assign_apps_to_positions(selected, positions)
    else:
        assignments = [(app, (0, 0, 960, 1080)) for app in selected]  # default position

    # Personaliza estas rutas
    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    nircmd_path = r"C:\Users\Florian\Downloads\snaplauncher\nir\nircmd.exe"

    generate_bat(assignments, chrome_path, nircmd_path)

import os
import win32com.client
from pathlib import Path
import tkinter
import re

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

def generate_close_script(assignments, filename="close_apps.py"):
    import re

    script_lines = [
        "import re",
        "import pygetwindow as gw",
        "",
        "# Lista de patrones para cerrar ventanas",
        "apps = ["
    ]

    for (name, path), (x, y, w, h) in assignments:
        pattern = re.escape(name.lower())
        script_lines.append(f"    r'{pattern}',")

    script_lines.append("]")
    script_lines.append("")
    script_lines.append("def close_windows():")
    script_lines.append("    all_windows = gw.getAllWindows()")
    script_lines.append("    closed = 0")
    script_lines.append("    for window in all_windows:")
    script_lines.append("        for pattern in apps:")
    script_lines.append("            if re.search(pattern, window.title, re.IGNORECASE):")
    script_lines.append("                try:")
    script_lines.append("                    window.close()")
    script_lines.append("                    print(f'✔ Cerrada ventana: {window.title}')")
    script_lines.append("                    closed += 1")
    script_lines.append("                except Exception as e:")
    script_lines.append("                    print(f'⚠ No se pudo cerrar ventana: {window.title} - {e}')")
    script_lines.append("                break")
    script_lines.append("    if closed == 0:")
    script_lines.append("        print('❌ No se encontraron ventanas para cerrar.')")
    script_lines.append("")
    script_lines.append("if __name__ == '__main__':")
    script_lines.append("    close_windows()")

    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(script_lines))

    print(f"\n✅ Script generado para cerrar ventanas: {filename}")
    print("Ejecuta con: python close_apps.py")


def generate_py_script(assignments, filename="launch_split.py"):
    import os

    script_lines = [
        "import subprocess",
        "import time",
        "import re",
        "import pygetwindow as gw",
        "",
        "# Lista de aplicaciones con sus posiciones y patrón regex para título",
        "apps = ["
    ]

    for (name, path), (x, y, w, h) in assignments:
        # Para el patrón regex usamos el nombre de la app, en minúsculas
        pattern = re.escape(name.lower())
        # Para command, cadena raw para evitar problemas con backslashes
        command = f'r"{path}"'
        script_lines.append("    {")
        script_lines.append(f"        'command': {command},")
        script_lines.append(f"        'pattern': r'{pattern}',")
        script_lines.append(f"        'position': ({x}, {y}, {w}, {h}),")
        script_lines.append("    },")
    script_lines.append("]")
    script_lines.append("")
    script_lines.append("def launch_and_position(app):")
    script_lines.append("    print(f\"Lanzando: {app['command']}\")")
    script_lines.append("    subprocess.Popen(app['command'], shell=True)")
    script_lines.append("    time.sleep(3)")
    script_lines.append("    window = None")
    script_lines.append("    for w in gw.getAllWindows():")
    script_lines.append("        if re.search(app['pattern'], w.title, re.IGNORECASE):")
    script_lines.append("            window = w")
    script_lines.append("            break")
    script_lines.append("    if window:")
    script_lines.append("        x, y, w_, h_ = app['position']")
    script_lines.append("        try:")
    script_lines.append("            window.moveTo(x, y)")
    script_lines.append("            window.resizeTo(w_, h_)")
    script_lines.append("            print(f\"✔ Posicionada: {window.title}\")")
    script_lines.append("        except Exception as e:")
    script_lines.append("            print(f\"⚠ No se pudo mover: {e}\")")
    script_lines.append("    else:")
    script_lines.append("        print(f\"❌ No se encontró ventana que coincida con el patrón: {app['pattern']}\")")
    script_lines.append("")
    script_lines.append("for app in apps:")
    script_lines.append("    launch_and_position(app)")
    script_lines.append("")
    script_lines.append("print('✅ Todas las apps fueron abiertas y posicionadas.')")

    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(script_lines))

    print(f"\n✅ Script generado: {filename}")
    print("Ejecuta con: python launch_split.py")

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
        # Posición por defecto si no se usa split
        assignments = [(app, (0, 0, 960, 1080)) for app in selected]

    generate_py_script(assignments)
    generate_close_script(assignments)

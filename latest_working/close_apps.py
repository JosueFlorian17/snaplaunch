import re
import pygetwindow as gw

# Lista de patrones para cerrar ventanas
apps = [
    r'word',
    r'xampp\ control\ panel',
    r'paint',
    r'zoom\ workplace',
]

def close_windows():
    all_windows = gw.getAllWindows()
    closed = 0
    for window in all_windows:
        for pattern in apps:
            if re.search(pattern, window.title, re.IGNORECASE):
                try:
                    window.close()
                    print(f'✔ Cerrada ventana: {window.title}')
                    closed += 1
                except Exception as e:
                    print(f'⚠ No se pudo cerrar ventana: {window.title} - {e}')
                break
    if closed == 0:
        print('❌ No se encontraron ventanas para cerrar.')

if __name__ == '__main__':
    close_windows()
import subprocess
import os
import platform

PROGRAMS = {
    "VSCode": "code",
    "Microsoft To-Do": "start ms-to-do:",
    "Calculadora": "calc",
    "Blender": r'"C:\Program Files\Blender Foundation\Blender 4.2\blender.exe"', 
}

def open_program(command):
    try:
        if platform.system() == "Windows":
            subprocess.run(command, shell=True)
        else:
            print(f"Este script aún no soporta {platform.system()}")
    except Exception as e:
        print(f"Error al abrir {command}: {e}")


for name, command in PROGRAMS.items():
    print(f"Abriendo {name}...")
    open_program(command)

print("✅ Todos los programas han sido iniciados.")

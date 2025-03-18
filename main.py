import webbrowser
import subprocess
import platform

study_mode_URLs = ["https://www.khanacademy.org/", "https://www.coursera.org/", "https://www.edx.org/"]
writing_mode_URLs = ["https://www.grammarly.com/", "https://www.hemingwayapp.com/", "https://www.grammarly.com/"]   
programming_mode_URLs = ["https://www.stackoverflow.com/", "https://www.github.com/", "https://www.codecademy.com/"]
entertainment_mode_URLs = ["https://www.youtube.com/", "https://www.netflix.com/", "https://www.twitch.tv/"]


programming_mode_Programs = {
    "VSCode": "code",
    "Microsoft To-Do": "start ms-to-do:",
    "Calculadora": "calc",
    "Blender": r'"C:\Program Files\Blender Foundation\Blender 4.3\blender.exe"', 
}
mode=input("Seleccione un modo: \n1.- Estudios\n2.- Redacción\n3.- Programación\n4.- Entretenimiento\n")


def open_program(command):
    try:
        if platform.system() == "Windows":
            subprocess.run(command, shell=True)
        else:
            print(f"Este script aún no soporta {platform.system()}")
    except Exception as e:
        print(f"Error al abrir {command}: {e}")

if mode == "1":
    for url in study_mode_URLs:
        webbrowser.open_new_tab(url)
elif mode == "2":
    for url in writing_mode_URLs:
        webbrowser.open_new_tab(url)
elif mode == "3":
    for url in programming_mode_URLs:
        webbrowser.open_new_tab(url)
    for name, command in programming_mode_Programs.items():
        print(f"Abriendo {name}...")
        open_program(command)
elif mode == "4":
    for url in entertainment_mode_URLs:
        webbrowser.open_new_tab(url)
else:
    print("Modo no válido")
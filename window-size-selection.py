import tkinter

def get_screen_resolution():
    root = tkinter.Tk()
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    root.destroy()
    return width, height

def print_previews():
    previews = {
        1: "┌──────┬──────┐\n│ App1 │ App2 │\n└──────┴──────┘",
        2: "┌──────┬──────┐\n│ App1 │ App2 │\n├──────┼──────┤\n│ App3 │ App4 │\n└──────┴──────┘",
        3: "┌────────┬────┐\n│ App1   │App2│\n│        ├────┤\n│        │App3│\n└────────┴────┘",
        4: "┌────┬────────┐\n│App1│        │\n├────┤  App3  │\n│App2│        │\n└────┴────────┘",
        5: "┌────────────┐\n│    App1     │\n├────────────┤\n│    App2     │\n└────────────┘"
    }
    print("\nModos de pantalla disponibles:\n")
    for i in range(1, 6):
        print(f"{i}.")
        print(previews[i])
        print()

def calculate_split(mode, width, height):
    print(f"\nResolución de pantalla: {width}x{height}")
    print(f"Modo {mode} seleccionado:")
    
    if mode == 1:  # Vertical doble
        w = width // 2
        h = height
        return [
            {"App": "App 1", "x": 0, "y": 0, "width": w, "height": h},
            {"App": "App 2", "x": w, "y": 0, "width": w, "height": h}
        ]
    
    elif mode == 2:  # Cuadrantes
        w = width // 2
        h = height // 2
        return [
            {"App": "App 1", "x": 0, "y": 0, "width": w, "height": h},
            {"App": "App 2", "x": w, "y": 0, "width": w, "height": h},
            {"App": "App 3", "x": 0, "y": h, "width": w, "height": h},
            {"App": "App 4", "x": w, "y": h, "width": w, "height": h}
        ]

    elif mode == 3:  # Grande izquierda, 2 derechas apiladas
        main_w = int(width * 0.66)
        side_w = width - main_w
        side_h = height // 2
        return [
            {"App": "App 1 (grande)", "x": 0, "y": 0, "width": main_w, "height": height},
            {"App": "App 2", "x": main_w, "y": 0, "width": side_w, "height": side_h},
            {"App": "App 3", "x": main_w, "y": side_h, "width": side_w, "height": side_h}
        ]

    elif mode == 4:  # 2 izquierdas, grande derecha
        main_w = int(width * 0.66)
        side_w = width - main_w
        side_h = height // 2
        return [
            {"App": "App 1", "x": 0, "y": 0, "width": side_w, "height": side_h},
            {"App": "App 2", "x": 0, "y": side_h, "width": side_w, "height": side_h},
            {"App": "App 3 (grande)", "x": side_w, "y": 0, "width": main_w, "height": height}
        ]

    elif mode == 5:  # Horizontal doble
        w = width
        h = height // 2
        return [
            {"App": "App 1", "x": 0, "y": 0, "width": w, "height": h},
            {"App": "App 2", "x": 0, "y": h, "width": w, "height": h}
        ]
    
    else:
        raise ValueError("Modo no válido.")

def main():
    width, height = get_screen_resolution()
    print_previews()
    
    try:
        mode = int(input("Selecciona el número del modo deseado (1-5): "))
        layout = calculate_split(mode, width, height)
        
        print("\nCoordenadas y tamaños de cada ventana:\n")
        for win in layout:
            print(f"{win['App']}: x={win['x']}, y={win['y']}, width={win['width']}, height={win['height']}")
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    main()

import tkinter

# Obtener la resolución de pantalla
root = tkinter.Tk()
width = root.winfo_screenwidth()
height = root.winfo_screenheight()
root.destroy()

print(f"Resolución de pantalla: {width}x{height}\n")
print("Modos de SplitScreen y sus resoluciones:")

# 1. Vertical Doble
print("\n1. Vertical Doble:")
w = width // 2
h = height
print(f"  App 1: x=0, y=0, width={w}, height={h}")
print(f"  App 2: x={w}, y=0, width={w}, height={h}")

# 2. Cuadrantes (2x2)
print("\n2. Cuadrantes:")
w = width // 2
h = height // 2
print(f"  App 1: x=0, y=0, width={w}, height={h}")
print(f"  App 2: x={w}, y=0, width={w}, height={h}")
print(f"  App 3: x=0, y={h}, width={w}, height={h}")
print(f"  App 4: x={w}, y={h}, width={w}, height={h}")

# 3. Principal Izquierda + 2 Derechas apiladas
print("\n3. Principal Izquierda + 2 Derechas:")
main_w = int(width * 0.66)
side_w = width - main_w
side_h = height // 2
print(f"  App 1 (grande): x=0, y=0, width={main_w}, height={height}")
print(f"  App 2: x={main_w}, y=0, width={side_w}, height={side_h}")
print(f"  App 3: x={main_w}, y={side_h}, width={side_w}, height={side_h}")

# 4. 2 Izquierdas + Principal Derecha
print("\n4. 2 Izquierdas + Principal Derecha:")
main_w = int(width * 0.66)
side_w = width - main_w
side_h = height // 2
print(f"  App 1: x=0, y=0, width={side_w}, height={side_h}")
print(f"  App 2: x=0, y={side_h}, width={side_w}, height={side_h}")
print(f"  App 3 (grande): x={side_w}, y=0, width={main_w}, height={height}")

# 5. Horizontal Doble
print("\n5. Horizontal Doble:")
w = width
h = height // 2
print(f"  App 1: x=0, y=0, width={w}, height={h}")
print(f"  App 2: x=0, y={h}, width={w}, height={h}")

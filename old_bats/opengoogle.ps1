# Abrir Google en Chrome (nueva ventana)
Start-Process "chrome.exe" "--new-window https://www.google.com"
Start-Sleep -Seconds 3  # Esperar que se abra

# Cargar funciones de la API de Windows
Add-Type @"
using System;
using System.Text;
using System.Runtime.InteropServices;

public class WinAPI {
    [DllImport("user32.dll")]
    public static extern bool EnumWindows(Func<IntPtr, int, bool> lpEnumFunc, int lParam);

    [DllImport("user32.dll")]
    public static extern bool IsWindowVisible(IntPtr hWnd);

    [DllImport("user32.dll")]
    public static extern int GetWindowText(IntPtr hWnd, StringBuilder lpString, int nMaxCount);

    [DllImport("user32.dll")]
    public static extern bool MoveWindow(IntPtr hWnd, int X, int Y, int nWidth, int nHeight, bool bRepaint);
}
"@

# Obtener dimensiones de pantalla
Add-Type -AssemblyName System.Windows.Forms
$screen = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds
$halfWidth = $screen.Width / 2
$height = $screen.Height

# Buscar ventana de Chrome
$chromeWindow = $null
[WinAPI]::EnumWindows({ 
    param($hWnd, $lParam)
    if ([WinAPI]::IsWindowVisible($hWnd)) {
        $title = New-Object System.Text.StringBuilder 256
        [WinAPI]::GetWindowText($hWnd, $title, $title.Capacity) | Out-Null
        if ($title.ToString() -like "*Google*") {
            $script:chromeWindow = $hWnd
            return $false  # detener búsqueda
        }
    }
    return $true
}, 0)

# Mover ventana si se encontró
if ($chromeWindow) {
    [WinAPI]::MoveWindow($chromeWindow, 0, 0, $halfWidth, $height, $true)  # Izquierda
} else {
    Write-Host "❌ No se encontró la ventana de Chrome con Google."
}

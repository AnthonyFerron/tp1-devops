param([Parameter(Mandatory=$true)][string]$Name)
$dir = "C:\Users\lebos\OneDrive\Bureau\Documents\Projets-g4\3eme annee\cours agile\tp1-devops\rapport\captures"
New-Item -ItemType Directory -Force -Path $dir | Out-Null
Add-Type @"
using System;
using System.Runtime.InteropServices;
public class WinCap {
  [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr h);
  [DllImport("user32.dll")] public static extern bool ShowWindow(IntPtr h, int n);
  [DllImport("user32.dll")] public static extern bool MoveWindow(IntPtr h, int x, int y, int w, int ht, bool repaint);
}
"@ -ErrorAction SilentlyContinue
$p = Get-Process chrome | Where-Object { $_.MainWindowHandle -ne 0 } | Select-Object -First 1
[WinCap]::ShowWindow($p.MainWindowHandle, 9) | Out-Null    # 9 = restore
Start-Sleep -Milliseconds 200
[WinCap]::MoveWindow($p.MainWindowHandle, 0, 0, 1040, 1040, $true) | Out-Null
[WinCap]::SetForegroundWindow($p.MainWindowHandle) | Out-Null
Start-Sleep -Milliseconds 1100
Add-Type -AssemblyName System.Windows.Forms,System.Drawing
# Chrome content area: skip the ~8px window border, capture inner page region
$cw = 1024; $ch = 1030
$bmp = New-Object System.Drawing.Bitmap($cw,$ch)
$g = [System.Drawing.Graphics]::FromImage($bmp)
$g.CopyFromScreen(8, 8, 0, 0, (New-Object System.Drawing.Size($cw,$ch)))
$path = Join-Path $dir "$Name.png"
$bmp.Save($path,[System.Drawing.Imaging.ImageFormat]::Png)
$g.Dispose(); $bmp.Dispose()
Write-Output "SAVED: $path ($((Get-Item $path).Length) bytes)"
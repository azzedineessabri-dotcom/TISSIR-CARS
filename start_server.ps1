$python = "C:\Users\aessabri\AppData\Local\Programs\Python\Python312\python.exe"
$code = @"
import sys
sys.path.insert(0, 'C:/Users/aessabri/car-rental')
from app import app
app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)
"@
$psi = New-Object System.Diagnostics.ProcessStartInfo
$psi.FileName = $python
$psi.Arguments = "-c `"$code`""
$psi.WorkingDirectory = 'C:\Users\aessabri\car-rental'
$psi.UseShellExecute = $false
$psi.CreateNoWindow = $true
$p = [System.Diagnostics.Process]::Start($psi)
Start-Sleep -Seconds 3
if (!$p.HasExited) {
    Write-Output "Flask started on PID $($p.Id)"
} else {
    Write-Output "Flask exited with code $($p.ExitCode)"
}

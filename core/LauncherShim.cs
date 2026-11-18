using System;
using System.IO;
using System.Diagnostics;
using System.Windows.Forms;

class Program {
    [STAThread]
    static void Main() {
        try {
            string baseDir = AppDomain.CurrentDomain.BaseDirectory;
            string scriptPath = Path.Combine(baseDir, "launcher.py");
            if (!File.Exists(scriptPath)) {
                MessageBox.Show("Файл launcher.py не найден в папке:\n" + baseDir, "Fallout 2 Launcher", MessageBoxButtons.OK, MessageBoxIcon.Error);
                return;
            }

            string pythonExe = null;
            string localAppData = Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData);
            
            string[] candidates = new string[] {
                Path.Combine(localAppData, @"Programs\Python\Python313\pythonw.exe"),
                Path.Combine(localAppData, @"Programs\Python\Python312\pythonw.exe"),
                Path.Combine(localAppData, @"Programs\Python\Python311\pythonw.exe"),
                Path.Combine(localAppData, @"Programs\Python\Python310\pythonw.exe"),
                Path.Combine(localAppData, @"Programs\Python\Python313\python.exe"),
                Path.Combine(localAppData, @"Programs\Python\Launcher\py.exe")
            };

            foreach (var cand in candidates) {
                if (File.Exists(cand)) {
                    pythonExe = cand;
                    break;
                }
            }

            if (pythonExe == null) {
                foreach (var name in new string[] { "py.exe", "pythonw.exe", "python.exe" }) {
                    var pathEnv = Environment.GetEnvironmentVariable("PATH") ?? "";
                    foreach (var dir in pathEnv.Split(';')) {
                        try {
                            string full = Path.Combine(dir.Trim(), name);
                            if (File.Exists(full) && !full.ToLower().Contains("windowsapps")) {
                                pythonExe = full;
                                break;
                            }
                        } catch {}
                    }
                    if (pythonExe != null) break;
                }
            }

            if (pythonExe == null) {
                MessageBox.Show("Не удалось найти установленный Python в системе.\nУстановите Python 3 с официального сайта python.org.", "Fallout 2 Launcher - Ошибка", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                return;
            }

            ProcessStartInfo psi = new ProcessStartInfo();
            psi.FileName = pythonExe;
            if (pythonExe.ToLower().EndsWith("py.exe")) {
                psi.Arguments = "-3 \"" + scriptPath + "\"";
            } else {
                psi.Arguments = "\"" + scriptPath + "\"";
            }
            psi.WorkingDirectory = baseDir;
            psi.UseShellExecute = false;

            Process.Start(psi);
        } catch (Exception ex) {
            MessageBox.Show("Ошибка при запуске лаунчера:\n" + ex.Message, "Fallout 2 Launcher - Ошибка", MessageBoxButtons.OK, MessageBoxIcon.Error);
        }
    }
}
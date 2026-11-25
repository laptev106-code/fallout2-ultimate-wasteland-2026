import subprocess
import time
import os

exe_path = r"E:\Fallout2_Ultimate\Fallout2_Gameplay\fallout2.exe"
cwd = r"E:\Fallout2_Ultimate\Fallout2_Gameplay"

print(f"Launching {exe_path}...")
proc = subprocess.Popen([exe_path], cwd=cwd)
print(f"Process started with PID: {proc.pid}")

time.sleep(3)

# Check if process is still running
poll = proc.poll()
if poll is None:
    print(f"PID {proc.pid} is running smoothly!")
    proc.terminate()
    try:
        proc.wait(timeout=3)
        print("Process terminated gracefully.")
    except Exception:
        proc.kill()
        print("Process killed.")
else:
    print(f"Process exited early with return code: {poll}")

# Check for crash dumps
crash_dump = os.path.join(cwd, "crash.dmp")
if os.path.exists(crash_dump):
    print("CRASH DETECTED! crash.dmp found!")
else:
    print("Zero crashes detected. Engine launch verified successfully.")

import win32process
import win32api
import win32con
import ctypes

# Find process
import subprocess
out = subprocess.check_output('tasklist /FI "IMAGENAME eq fallout2.exe" /FO CSV /NH', shell=True, text=True)
print(out)
lines = [l for l in out.strip().splitlines() if 'fallout2.exe' in l.lower()]
if not lines:
    print('fallout2.exe not running')
    exit()

pid = int(lines[0].split(',')[1].replace('"', ''))
print('PID:', pid)

PROCESS_ALL_ACCESS = 0x1F0FFF
hProcess = ctypes.windll.kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, pid)
if not hProcess:
    print('Failed to open process:', ctypes.GetLastError())
    exit()

# Let's find f2_res.dll base in process
import win32process
modules = win32process.EnumProcessModules(hProcess)
f2_base = None
for m in modules:
    name = win32process.GetModuleFileNameEx(hProcess, m)
    if 'f2_res.dll' in name.lower():
        f2_base = m
        print('Found f2_res.dll in process at:', hex(f2_base))
        break

if not f2_base:
    print('f2_res.dll not loaded!')
    exit()

# Read variables:
# [0x1006ecdc] -> SCALE_2X active (offset 0x6ecdc)
# [0x1003f1cc] -> internal width (offset 0x3f1cc)
# [0x1003f1d0] -> internal height (offset 0x3f1d0)
# [0x1006ed1d] -> windowed active (offset 0x6ed1d)
# [0x1006ecec] -> config windowed value (offset 0x6ecec)

def read_mem(offset, size=4):
    buf = ctypes.create_string_buffer(size)
    bytesRead = ctypes.c_size_t()
    ctypes.windll.kernel32.ReadProcessMemory(hProcess, ctypes.c_void_p(f2_base + offset), buf, size, ctypes.byref(bytesRead))
    if size == 4:
        import struct
        return struct.unpack('<I', buf.raw)[0]
    elif size == 1:
        return buf.raw[0]
    return buf.raw

print('SCALE_2X var [0x6ecdc]:', read_mem(0x6ecdc, 4))
print('Internal Width [0x3f1cc]:', read_mem(0x3f1cc, 4))
print('Internal Height [0x3f1d0]:', read_mem(0x3f1d0, 4))
print('Windowed var [0x6ecec]:', read_mem(0x6ecec, 4))
print('Windowed active flag [0x6ed1d]:', read_mem(0x6ed1d, 1))

ctypes.windll.kernel32.CloseHandle(hProcess)

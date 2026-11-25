import pefile

with open(r'E:\Fallout2_Ultimate\Fallout2_Gameplay\f2_res.dll', 'rb') as f:
    data = f.read()

pe = pefile.PE(r'E:\Fallout2_Ultimate\Fallout2_Gameplay\f2_res.dll')
def va_to_str(va):
    rva = va - pe.OPTIONAL_HEADER.ImageBase
    for s in pe.sections:
        if s.VirtualAddress <= rva < s.VirtualAddress + s.Misc_VirtualSize:
            raw = s.PointerToRawData + (rva - s.VirtualAddress)
            end = data.find(b'\x00', raw)
            return data[raw:end].decode('ascii', errors='ignore')
    return ''

print(hex(0x1003a3d4), va_to_str(0x1003a3d4))
print(hex(0x1003a3e0), va_to_str(0x1003a3e0))

import os

p_glasses = r"D:\AG games mods\fallout2-ultimate-wasteland-2026\tools\gl_glasses.ssl"
with open(p_glasses, "r", encoding="cp1251") as f:
    c = f.read()
c = c.replace('#include "define.h"', '#include "headers/define.h"')
c = c.replace('#include "sfall/sfall.h"', '#include "headers/sfall/sfall.h"')
with open(p_glasses, "w", encoding="cp1251") as f:
    f.write(c)

p_laststand = r"D:\AG games mods\fallout2-ultimate-wasteland-2026\tools\gl_laststand.ssl"
with open(p_laststand, "r", encoding="cp1251") as f:
    c = f.read()
c = c.replace('#include "define.h"', '#include "headers/define.h"')
c = c.replace('#include "command.h"', '#include "headers/command.h"')
c = c.replace('#include "sfall/sfall.h"', '#include "headers/sfall/sfall.h"')
c = c.replace('#include "sfall/define_extra.h"', '#include "headers/sfall/define_extra.h"')
c = c.replace('#include "sfall/lib.arrays.h"', '#include "headers/sfall/lib.arrays.h"')
with open(p_laststand, "w", encoding="cp1251") as f:
    f.write(c)

print("Updated includes successfully")

# -*- coding: utf-8 -*-
with open(r"E:\FALLOUT Ult pjt\tools\kcyellow.int", "rb") as f:
    data = f.read()

# Let's inspect bytes between 1ab0 and 1b30
# 1ac8: c0 01 00 00 1b 1c ...
# In Fallout opcode: 0x80bf = obj_is_carrying / dude_item_count?
# Let's look at 0x11c = 284 = PID_MEAT_JERKY (71) or PID_DRYMEAT (284 = 0x11c!)
# 0x011c is 284! In itempid.h: PID_MEAT_JERKY or PID_DRYMEAT or PID_RADSCORPION_PARTS?
# Let's check PID 284 in itempid.h!

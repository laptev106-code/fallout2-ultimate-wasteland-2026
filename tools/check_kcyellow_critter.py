# -*- coding: utf-8 -*-
with open(r"E:\FALLOUT Ult pjt\tools\kcyellow.int", "rb") as f:
    data = f.read()

# Let's search for obj_can_see_obj or tile_distance in kcyellow.int
# In Fallout: tile_distance_objs(self_obj, dude_obj)
# or dialog_proc
print("data size:", len(data))

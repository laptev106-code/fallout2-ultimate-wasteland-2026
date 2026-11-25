path = r"d:\AG games mods\fallout2-ultimate-wasteland-2026\tools\gl_temple_hints.ssl"
with open(path, "r", encoding="cp1251", errors="ignore") as f:
    text = f.read()

target = '            display_msg("Keep your eyes peeled in the gloom. Press TAB to spot gear and containers, and F1 for key controls.");\n            display_msg("Check every clay urn and pot along the walls. The tribal elders loved tucking away supplies in old pottery.");\n         end else begin\n            display_msg("В полумраке святилища держи ухо востро. Клавиша TAB подсветит вещи и сундуки, а F1 откроет памятку по кнопкам.");'

replacement = '            display_msg("Keep your eyes peeled in the gloom. Hold Shift to highlight gear, traps, and containers, and press F1 for key controls.");\n            display_msg("Check every clay urn and pot along the walls. The tribal elders loved tucking away supplies in old pottery.");\n         end else begin\n            display_msg("В полумраке святилища держи ухо востро. Зажми клавишу Shift, чтобы подсветить вещи, ловушки и сундуки, а F1 откроет памятку по кнопкам.");'

if target in text:
    text = text.replace(target, replacement)
    with open(path, "w", encoding="cp1251", errors="ignore") as f:
        f.write(text)
    print("Replaced successfully!")
else:
    print("Target not found, checking with normalize...")
    # fallback
    text = text.replace("Press TAB to spot gear and containers", "Hold Shift to highlight gear, traps, and containers")
    text = text.replace("Клавиша TAB подсветит вещи и сундуки", "Зажми клавишу Shift, чтобы подсветить вещи, ловушки и сундуки")
    with open(path, "w", encoding="cp1251", errors="ignore") as f:
        f.write(text)
    print("Fallback replaced!")

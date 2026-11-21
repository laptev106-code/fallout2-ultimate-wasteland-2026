import re

# 1. Update index.html
html_path = r"D:\AG games mods\fallout2-ultimate-wasteland-2026\launcher_nextgen\ui\index.html"
with open(html_path, "r", encoding="utf-8") as f:
    html = f.read()

target_group = """                <div class="form-group">
                  <label class="diag-checkbox-label" style="margin-top: 8px; display: flex; align-items: center; gap: 10px; cursor: pointer;">
                    <input id="toggle-alwaysrun" type="checkbox" checked style="width: 18px; height: 18px; accent-color: var(--green-primary);">
                    <span style="font-size: 13px; color: var(--text-main);">Всегда бегать (Auto-Run по умолчанию)</span>
                  </label>
                </div>"""

new_group = """                <div class="form-group">
                  <label class="diag-checkbox-label" style="margin-top: 8px; display: flex; align-items: center; gap: 10px; cursor: pointer;">
                    <input id="toggle-alwaysrun" type="checkbox" checked style="width: 18px; height: 18px; accent-color: var(--green-primary);">
                    <span style="font-size: 13px; color: var(--text-main);">Всегда бегать (Auto-Run по умолчанию)</span>
                  </label>
                </div>

                <div class="form-group">
                  <label class="diag-checkbox-label" style="margin-top: 8px; display: flex; align-items: center; gap: 10px; cursor: pointer;">
                    <input id="toggle-temple-tutorial" type="checkbox" checked style="width: 18px; height: 18px; accent-color: var(--green-primary);">
                    <span style="font-size: 13px; color: var(--text-main);">Обучающие подсказки в Храме Испытаний (советы по механике, клавишам и выживанию)</span>
                  </label>
                </div>"""

if target_group in html:
    html = html.replace(target_group, new_group)
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)
    print("Updated index.html with temple tutorial toggle")
else:
    print("target_group not found in index.html")

# 2. Update app.js
js_path = r"D:\AG games mods\fallout2-ultimate-wasteland-2026\launcher_nextgen\ui\js\app.js"
with open(js_path, "r", encoding="utf-8") as f:
    js = f.read()

# Listener update
js = js.replace(
    "'toggle-autoreload', 'toggle-alwaysrun'",
    "'toggle-autoreload', 'toggle-alwaysrun', 'toggle-temple-tutorial'"
)

# applyConfigToUI update
target_apply = """    const chkRun = document.getElementById('toggle-alwaysrun');
    if (chkRun) chkRun.checked = this.config.alwaysRun !== false;"""

new_apply = """    const chkRun = document.getElementById('toggle-alwaysrun');
    if (chkRun) chkRun.checked = this.config.alwaysRun !== false;

    const chkTutorial = document.getElementById('toggle-temple-tutorial');
    if (chkTutorial) chkTutorial.checked = this.config.templeTutorial !== false;"""

js = js.replace(target_apply, new_apply)

# saveCurrentSettings update
target_save = """    const chkReload = document.getElementById('toggle-autoreload');
    const chkRun = document.getElementById('toggle-alwaysrun');"""

new_save = """    const chkReload = document.getElementById('toggle-autoreload');
    const chkRun = document.getElementById('toggle-alwaysrun');
    const chkTutorial = document.getElementById('toggle-temple-tutorial');"""

js = js.replace(target_save, new_save)

target_cfg = """      autoReload: chkReload ? chkReload.checked : false,
      alwaysRun: chkRun ? chkRun.checked : true"""

new_cfg = """      autoReload: chkReload ? chkReload.checked : false,
      alwaysRun: chkRun ? chkRun.checked : true,
      templeTutorial: chkTutorial ? chkTutorial.checked : true"""

js = js.replace(target_cfg, new_cfg)

with open(js_path, "w", encoding="utf-8") as f:
    f.write(js)
print("Updated app.js with temple tutorial toggle")

import os

# 1. Update index.html
html_path = r"D:\AG games mods\fallout2-ultimate-wasteland-2026\launcher_nextgen\ui\index.html"
with open(html_path, "r", encoding="utf-8") as f:
    html = f.read()

target_html = """                <div class="form-group">
                  <div class="form-label-block">
                    <span class="form-label">ЗВУКОВЫЕ ЭФФЕКТЫ (SFX):</span>
                    <span class="form-hint">Громкость выстрелов, шагов и взрывов.</span>
                  </div>
                  <div class="slider-container">
                    <input id="slider-sfx" type="range" min="0" max="100" value="80" class="form-slider">
                    <span id="val-sfx" class="slider-val">80%</span>
                  </div>
                </div>
              </div>

              <button id="btn-save-settings" class="btn-primary">"""

new_qol_section = """                <div class="form-group">
                  <div class="form-label-block">
                    <span class="form-label">ЗВУКОВЫЕ ЭФФЕКТЫ (SFX):</span>
                    <span class="form-hint">Громкость выстрелов, шагов и взрывов.</span>
                  </div>
                  <div class="slider-container">
                    <input id="slider-sfx" type="range" min="0" max="100" value="80" class="form-slider">
                    <span id="val-sfx" class="slider-val">80%</span>
                  </div>
                </div>
              </div>

              <div class="section-box">
                <div class="section-title">ИГРОВОЙ ПРОЦЕСС И УДОБСТВО (QoL)</div>
                <div class="section-desc">Опции автоматизации рутины и комфорта управления персонажем.</div>

                <div class="form-group">
                  <label class="diag-checkbox-label" style="margin-top: 4px; display: flex; align-items: center; gap: 10px; cursor: pointer;">
                    <input id="toggle-autoreload" type="checkbox" style="width: 18px; height: 18px; accent-color: var(--green-primary);">
                    <span style="font-size: 13px; color: var(--text-main);">Автоматическая перезарядка оружия после боя (пополнение патронов из рюкзака)</span>
                  </label>
                </div>

                <div class="form-group">
                  <label class="diag-checkbox-label" style="margin-top: 8px; display: flex; align-items: center; gap: 10px; cursor: pointer;">
                    <input id="toggle-alwaysrun" type="checkbox" checked style="width: 18px; height: 18px; accent-color: var(--green-primary);">
                    <span style="font-size: 13px; color: var(--text-main);">Всегда бегать (Auto-Run по умолчанию)</span>
                  </label>
                </div>
              </div>

              <button id="btn-save-settings" class="btn-primary">"""

if target_html in html:
    html = html.replace(target_html, new_qol_section)
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)
    print("Updated index.html")
else:
    print("Could not find target_html in index.html")

# 2. Update app.js
js_path = r"D:\AG games mods\fallout2-ultimate-wasteland-2026\launcher_nextgen\ui\js\app.js"
with open(js_path, "r", encoding="utf-8") as f:
    js = f.read()

# Add listener
old_listeners = "['select-res', 'select-mode', 'select-scale', 'select-filter'].forEach(id => {"
new_listeners = "['select-res', 'select-mode', 'select-scale', 'select-filter', 'toggle-autoreload', 'toggle-alwaysrun'].forEach(id => {"
if old_listeners in js:
    js = js.replace(old_listeners, new_listeners)
    print("Updated listeners in app.js")

# Add applyConfigToUI
old_apply = """    const sSfx = document.getElementById('slider-sfx');
    if (sSfx && this.config.sfxVol !== undefined) {
      sSfx.value = this.config.sfxVol;
      document.getElementById('val-sfx').textContent = `${sSfx.value}%`;
    }"""

new_apply = """    const sSfx = document.getElementById('slider-sfx');
    if (sSfx && this.config.sfxVol !== undefined) {
      sSfx.value = this.config.sfxVol;
      document.getElementById('val-sfx').textContent = `${sSfx.value}%`;
    }

    const chkReload = document.getElementById('toggle-autoreload');
    if (chkReload) chkReload.checked = !!this.config.autoReload;

    const chkRun = document.getElementById('toggle-alwaysrun');
    if (chkRun) chkRun.checked = this.config.alwaysRun !== false;"""

if old_apply in js:
    js = js.replace(old_apply, new_apply)
    print("Updated applyConfigToUI in app.js")

# Add saveCurrentSettings
old_save = """    const cfg = {
      resolution: selRes ? selRes.value : '2560x1440',
      mode: selMode ? selMode.value : 'borderless',
      scale: selScale ? selScale.value : '2x',
      filtering: selFilter ? selFilter.value : 'bilinear',
      musicVol: sMusic ? parseInt(sMusic.value, 10) : 80,
      sfxVol: sSfx ? parseInt(sSfx.value, 10) : 80
    };"""

new_save = """    const chkReload = document.getElementById('toggle-autoreload');
    const chkRun = document.getElementById('toggle-alwaysrun');

    const cfg = {
      resolution: selRes ? selRes.value : '2560x1440',
      mode: selMode ? selMode.value : 'borderless',
      scale: selScale ? selScale.value : '2x',
      filtering: selFilter ? selFilter.value : 'bilinear',
      musicVol: sMusic ? parseInt(sMusic.value, 10) : 80,
      sfxVol: sSfx ? parseInt(sSfx.value, 10) : 80,
      autoReload: chkReload ? chkReload.checked : false,
      alwaysRun: chkRun ? chkRun.checked : true
    };"""

if old_save in js:
    js = js.replace(old_save, new_save)
    with open(js_path, "w", encoding="utf-8") as f:
        f.write(js)
    print("Updated saveCurrentSettings in app.js")
else:
    print("Could not find old_save in app.js")

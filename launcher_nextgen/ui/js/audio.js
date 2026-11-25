/**
 * Pip-Boy Audio Engine (Fallout 2 Authentic Sound FX).
 * Plays genuine 1998 Fallout 2 mechanical relay clicks, tab switches, CRT hum, and launcher cues.
 */
class PipBoyAudioEngine {
  constructor() {
    this.ctx = null;
    const savedSound = localStorage.getItem('nextgen_sound_enabled');
    this.enabled = savedSound === null ? true : (savedSound === 'true');
    const savedHum = localStorage.getItem('nextgen_hum_enabled');
    this.humEnabled = savedHum === null ? true : (savedHum === 'true');
    this.buffers = {};
    this.humNode = null;
    this.audioPaths = {
      click: 'assets/audio/click.wav',
      tab: 'assets/audio/tab.wav',
      toggle: 'assets/audio/toggle.wav',
      launch: 'assets/audio/launch.wav',
      hum: 'assets/audio/crt_hum.wav'
    };
    this.initAudioContext();
    this.loadAudioFiles();
    this.setupUserUnlock();
  }

  initAudioContext() {
    try {
      const AudioCtx = window.AudioContext || window.webkitAudioContext;
      if (AudioCtx) {
        this.ctx = new AudioCtx();
      }
    } catch (e) {
      console.warn("WebAudio initialization warning:", e);
    }
  }

  setupUserUnlock() {
    // If WebAudio was locked/suspended by Edge WebView2 sandbox, wake it on the first user interaction
    const unlock = () => {
      if (this.ctx) {
        if (this.ctx.state === 'suspended') {
          this.ctx.resume().then(() => {
            if (this.enabled && this.humEnabled && !this.humNode) {
              this.startCrtHum();
            }
          });
        } else if (this.enabled && this.humEnabled && !this.humNode) {
          this.startCrtHum();
        }
      }
      window.removeEventListener('pointerdown', unlock);
      window.removeEventListener('keydown', unlock);
      window.removeEventListener('click', unlock);
    };
    window.addEventListener('pointerdown', unlock);
    window.addEventListener('keydown', unlock);
    window.addEventListener('click', unlock);
  }

  async loadAudioFiles() {
    if (!this.ctx) return;
    for (const [key, path] of Object.entries(this.audioPaths)) {
      try {
        const response = await fetch(path);
        if (response.ok) {
          const arrayBuffer = await response.arrayBuffer();
          this.buffers[key] = await this.ctx.decodeAudioData(arrayBuffer);
        }
      } catch (err) {
        console.warn(`Could not preload audio asset [${key}]:`, err);
      }
    }
  }

  resume() {
    if (this.ctx && this.ctx.state === 'suspended') {
      return this.ctx.resume();
    }
    return Promise.resolve();
  }

  playBuffer(name, fallbackFn, customGain = 0.5) {
    if (!this.enabled) return;
    this.resume();

    if (this.buffers[name] && this.ctx) {
      try {
        const src = this.ctx.createBufferSource();
        src.buffer = this.buffers[name];
        const gain = this.ctx.createGain();
        gain.gain.setValueAtTime(customGain, this.ctx.currentTime);
        src.connect(gain);
        gain.connect(this.ctx.destination);
        src.start(0);
        return;
      } catch (e) {
        console.warn("Buffer playback fallback:", e);
      }
    }

    if (fallbackFn) fallbackFn();
  }

  // --- CRT HUM (Seamless pre-rendered WAV loop — zero oscillator jitter/pulsing) ---
  startCrtHum() {
    if (!this.enabled || !this.humEnabled || this.humNode || this._humStarting || !this.ctx) return;
    this._humStarting = true;
    this.resume().then(() => {
      this._humStarting = false;
      try {
        if (!this.enabled || !this.humEnabled || this.humNode) return;
        const t = this.ctx.currentTime;

        if (this.buffers.hum) {
          const src = this.ctx.createBufferSource();
          src.buffer = this.buffers.hum;
          src.loop = true;

          const gain = this.ctx.createGain();
          gain.gain.setValueAtTime(0.0001, t);
          gain.gain.linearRampToValueAtTime(0.14, t + 0.5);

          src.connect(gain);
          gain.connect(this.ctx.destination);
          src.start(t);

          this.humNode = { src, gain };
        }
      } catch (e) {
        console.warn("Could not start CRT hum:", e);
      }
    });
  }

  stopCrtHum() {
    this._humStarting = false;
    if (!this.humNode || !this.ctx) return;
    try {
      const t = this.ctx.currentTime;
      const { gain } = this.humNode;
      gain.gain.cancelScheduledValues(t);
      gain.gain.setValueAtTime(gain.gain.value, t);
      gain.gain.linearRampToValueAtTime(0.0001, t + 0.12);
      const node = this.humNode;
      this.humNode = null;
      setTimeout(() => {
        try {
          node.src.stop();
          node.src.disconnect();
          node.gain.disconnect();
        } catch (_) {}
      }, 140);
    } catch (e) {
      this.humNode = null;
    }
  }

  // --- LAUNCHER BOOT-UP SOUND ---
  playLauncherBoot() {
    if (!this.enabled || !this.ctx) return;
    this.resume().then(() => {
      try {
        const t = this.ctx.currentTime;

        // 1. Soft mechanical power rocker switch click (zero high-pitched beep)
        const oscSwitch = this.ctx.createOscillator();
        const gainSwitch = this.ctx.createGain();
        oscSwitch.type = 'triangle';
        oscSwitch.frequency.setValueAtTime(240, t);
        oscSwitch.frequency.exponentialRampToValueAtTime(60, t + 0.025);
        gainSwitch.gain.setValueAtTime(0.08, t);
        gainSwitch.gain.exponentialRampToValueAtTime(0.001, t + 0.028);
        oscSwitch.connect(gainSwitch);
        gainSwitch.connect(this.ctx.destination);
        oscSwitch.start(t);
        oscSwitch.stop(t + 0.03);

        // 2. Warm CRT tube degauss coil thump (lamp TV power-on resonance)
        const oscDegauss = this.ctx.createOscillator();
        const filterDegauss = this.ctx.createBiquadFilter();
        const gainDegauss = this.ctx.createGain();
        oscDegauss.type = 'sine';
        oscDegauss.frequency.setValueAtTime(95, t + 0.02);
        oscDegauss.frequency.exponentialRampToValueAtTime(46, t + 0.36);

        filterDegauss.type = 'lowpass';
        filterDegauss.frequency.setValueAtTime(160, t);

        gainDegauss.gain.setValueAtTime(0.001, t);
        gainDegauss.gain.linearRampToValueAtTime(0.11, t + 0.05);
        gainDegauss.gain.exponentialRampToValueAtTime(0.001, t + 0.38);

        oscDegauss.connect(filterDegauss);
        filterDegauss.connect(gainDegauss);
        gainDegauss.connect(this.ctx.destination);
        oscDegauss.start(t + 0.02);
        oscDegauss.stop(t + 0.40);

        // 3. Start CRT hum automatically after warm-up (only if hum is enabled)
        setTimeout(() => {
          if (this.enabled && this.humEnabled && !this.humNode) {
            this.startCrtHum();
          }
        }, 280);
      } catch (e) {
        console.warn("Error playing launcher boot sound:", e);
      }
    });
  }

  // --- GAME LAUNCH SOUND (Clean double mechanical Fallout 2 relay latch — zero harshness) ---
  playGameLaunch() {
    if (!this.enabled || !this.ctx) return;
    this.resume();
    try {
      this.playBuffer('toggle', () => this._syntheticSnap(0.18), 0.26);
      setTimeout(() => {
        if (this.enabled) {
          this.playBuffer('click', () => this._syntheticRelay(0.16), 0.22);
        }
      }, 95);
    } catch (e) {
      this._syntheticRelay(0.15);
    }
  }

  // Alias for backward compatibility
  playLaunchSiren() {
    this.playGameLaunch();
  }

  playRelayClick() {
    this.playBuffer('click', () => this._syntheticRelay(0.25), 0.35);
  }

  playSwitchSnap() {
    this.playBuffer('toggle', () => this._syntheticSnap(0.22), 0.32);
  }

  playTabSwitch() {
    this.playBuffer('tab', () => this._syntheticRelay(0.20), 0.28);
  }

  playPipClick() {
    this._syntheticRelay(0.16);
  }

  playPipSelect() {
    this._syntheticSnap(0.18);
  }

  // Fallback WebAudio synthesisers
  _syntheticRelay(vol = 0.25) {
    if (!this.ctx) return;
    const t = this.ctx.currentTime;
    const osc = this.ctx.createOscillator();
    const gain = this.ctx.createGain();
    osc.type = 'triangle';
    osc.frequency.setValueAtTime(1100, t);
    osc.frequency.exponentialRampToValueAtTime(140, t + 0.035);
    gain.gain.setValueAtTime(vol, t);
    gain.gain.exponentialRampToValueAtTime(0.001, t + 0.035);
    osc.connect(gain);
    gain.connect(this.ctx.destination);
    osc.start(t);
    osc.stop(t + 0.04);
  }

  _syntheticSnap(vol = 0.22) {
    if (!this.ctx) return;
    const t = this.ctx.currentTime;
    const osc = this.ctx.createOscillator();
    const gain = this.ctx.createGain();
    osc.type = 'square';
    osc.frequency.setValueAtTime(420, t);
    osc.frequency.exponentialRampToValueAtTime(75, t + 0.045);
    gain.gain.setValueAtTime(vol, t);
    gain.gain.exponentialRampToValueAtTime(0.001, t + 0.045);
    osc.connect(gain);
    gain.connect(this.ctx.destination);
    osc.start(t);
    osc.stop(t + 0.05);
  }

  toggleSound() {
    this.enabled = !this.enabled;
    localStorage.setItem('nextgen_sound_enabled', String(this.enabled));
    if (this.enabled) {
      if (this.humEnabled) this.startCrtHum();
      this.playSwitchSnap();
    } else {
      this.stopCrtHum();
    }
    return this.enabled;
  }

  toggleHum() {
    this.humEnabled = !this.humEnabled;
    localStorage.setItem('nextgen_hum_enabled', String(this.humEnabled));
    if (this.humEnabled && this.enabled) {
      this.startCrtHum();
    } else {
      this.stopCrtHum();
    }
    return this.humEnabled;
  }
}

// Global singleton instance
window.pipAudio = new PipBoyAudioEngine();

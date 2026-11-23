/**
 * Pip-Boy Audio Engine (Fallout 2 Authentic Sound FX).
 * Plays genuine 1998 Fallout 2 mechanical relay clicks, tab switches, CRT hum, and launcher cues.
 */
class PipBoyAudioEngine {
  constructor() {
    this.ctx = null;
    this.enabled = true;
    this.buffers = {};
    this.humNode = null;
    this.audioPaths = {
      click: 'assets/audio/click.wav',
      tab: 'assets/audio/tab.wav',
      toggle: 'assets/audio/toggle.wav',
      launch: 'assets/audio/launch.wav'
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
            if (this.enabled && !this.humNode) {
              this.startCrtHum();
            }
          });
        } else if (this.enabled && !this.humNode) {
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

  // --- CRT HUM (Continuous atmospheric 50Hz/100Hz power hum) ---
  startCrtHum() {
    if (!this.enabled || this.humNode || !this.ctx) return;
    this.resume().then(() => {
      try {
        if (this.humNode) return;
        const t = this.ctx.currentTime;

        // 50Hz main power transformer oscillation
        const osc50 = this.ctx.createOscillator();
        osc50.type = 'sawtooth';
        osc50.frequency.setValueAtTime(50, t);

        // 100Hz harmonic
        const osc100 = this.ctx.createOscillator();
        osc100.type = 'sine';
        osc100.frequency.setValueAtTime(100, t);

        // Subtle 15.6 kHz cathode line-scan resonance
        const oscCathode = this.ctx.createOscillator();
        oscCathode.type = 'sine';
        oscCathode.frequency.setValueAtTime(15625, t);

        // Low-pass filter for smooth, non-fatiguing warm tone
        const filter = this.ctx.createBiquadFilter();
        filter.type = 'lowpass';
        filter.frequency.setValueAtTime(180, t);
        filter.Q.setValueAtTime(1.2, t);

        const gainMain = this.ctx.createGain();
        gainMain.gain.setValueAtTime(0.0001, t);
        // Soft ramp up to comfortable level
        gainMain.gain.linearRampToValueAtTime(0.022, t + 0.4);

        const gainCathode = this.ctx.createGain();
        gainCathode.gain.setValueAtTime(0.0001, t);
        gainCathode.gain.linearRampToValueAtTime(0.0025, t + 0.8);

        osc50.connect(filter);
        osc100.connect(filter);
        filter.connect(gainMain);
        gainMain.connect(this.ctx.destination);

        oscCathode.connect(gainCathode);
        gainCathode.connect(this.ctx.destination);

        osc50.start(t);
        osc100.start(t);
        oscCathode.start(t);

        this.humNode = { osc50, osc100, oscCathode, gainMain, gainCathode, filter };
      } catch (e) {
        console.warn("Could not start CRT hum:", e);
      }
    });
  }

  stopCrtHum() {
    if (!this.humNode || !this.ctx) return;
    try {
      const t = this.ctx.currentTime;
      this.humNode.gainMain.gain.linearRampToValueAtTime(0.0001, t + 0.1);
      this.humNode.gainCathode.gain.linearRampToValueAtTime(0.0001, t + 0.1);
      const node = this.humNode;
      this.humNode = null;
      setTimeout(() => {
        try {
          node.osc50.stop();
          node.osc100.stop();
          node.oscCathode.stop();
          node.osc50.disconnect();
          node.osc100.disconnect();
          node.oscCathode.disconnect();
        } catch (_) {}
      }, 120);
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

        // Cathode high-frequency charge pulse (warm-up)
        const oscBoot = this.ctx.createOscillator();
        const gainBoot = this.ctx.createGain();
        oscBoot.type = 'sawtooth';
        oscBoot.frequency.setValueAtTime(2200, t);
        oscBoot.frequency.exponentialRampToValueAtTime(140, t + 0.08);

        gainBoot.gain.setValueAtTime(0.18, t);
        gainBoot.gain.exponentialRampToValueAtTime(0.001, t + 0.08);

        oscBoot.connect(gainBoot);
        gainBoot.connect(this.ctx.destination);
        oscBoot.start(t);
        oscBoot.stop(t + 0.085);

        // Power relay latch 1
        setTimeout(() => this._syntheticRelay(0.18), 90);
        // Power relay latch 2
        setTimeout(() => this._syntheticRelay(0.22), 170);

        // Start CRT hum automatically after boot chime
        setTimeout(() => {
          if (this.enabled && !this.humNode) {
            this.startCrtHum();
          }
        }, 220);
      } catch (e) {
        console.warn("Error playing launcher boot sound:", e);
      }
    });
  }

  // --- GAME LAUNCH SOUND (New: Deep mechanical Vault latch & hydraulic lock, gentle volume) ---
  playGameLaunch() {
    if (!this.enabled || !this.ctx) return;
    this.resume();
    try {
      const t = this.ctx.currentTime;

      // 1. Deep hydraulic servo clunk
      const oscHydraulic = this.ctx.createOscillator();
      const gainHydraulic = this.ctx.createGain();
      const filter = this.ctx.createBiquadFilter();

      oscHydraulic.type = 'square';
      oscHydraulic.frequency.setValueAtTime(160, t);
      oscHydraulic.frequency.exponentialRampToValueAtTime(42, t + 0.28);

      filter.type = 'lowpass';
      filter.frequency.setValueAtTime(280, t);

      gainHydraulic.gain.setValueAtTime(0.22, t);
      gainHydraulic.gain.exponentialRampToValueAtTime(0.001, t + 0.28);

      oscHydraulic.connect(filter);
      filter.connect(gainHydraulic);
      gainHydraulic.connect(this.ctx.destination);

      oscHydraulic.start(t);
      oscHydraulic.stop(t + 0.29);

      // 2. Heavy mechanical vault latch engagement
      const oscLatch = this.ctx.createOscillator();
      const gainLatch = this.ctx.createGain();
      oscLatch.type = 'triangle';
      oscLatch.frequency.setValueAtTime(480, t + 0.05);
      oscLatch.frequency.exponentialRampToValueAtTime(95, t + 0.22);

      gainLatch.gain.setValueAtTime(0.001, t);
      gainLatch.gain.setValueAtTime(0.19, t + 0.05);
      gainLatch.gain.exponentialRampToValueAtTime(0.001, t + 0.22);

      oscLatch.connect(gainLatch);
      gainLatch.connect(this.ctx.destination);

      oscLatch.start(t + 0.05);
      oscLatch.stop(t + 0.23);
    } catch (e) {
      this._syntheticRelay(0.3);
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
    if (this.enabled) {
      this.startCrtHum();
      this.playSwitchSnap();
    } else {
      this.stopCrtHum();
    }
    return this.enabled;
  }
}

// Global singleton instance
window.pipAudio = new PipBoyAudioEngine();

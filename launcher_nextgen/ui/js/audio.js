/**
 * Pip-Boy Audio Engine (Fallout 2 Authentic Sound FX).
 * Plays genuine 1998 Fallout 2 mechanical relay clicks, tab switches, and launch cues.
 */
class PipBoyAudioEngine {
  constructor() {
    this.ctx = null;
    this.enabled = true;
    this.buffers = {};
    this.audioPaths = {
      click: 'assets/audio/click.wav',
      tab: 'assets/audio/tab.wav',
      toggle: 'assets/audio/toggle.wav',
      launch: 'assets/audio/launch.wav'
    };
    this.initAudioContext();
    this.loadAudioFiles();
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
      this.ctx.resume();
    }
  }

  playBuffer(name, fallbackFn) {
    if (!this.enabled) return;
    this.resume();

    if (this.buffers[name] && this.ctx) {
      try {
        const src = this.ctx.createBufferSource();
        src.buffer = this.buffers[name];
        const gain = this.ctx.createGain();
        gain.gain.setValueAtTime(0.7, this.ctx.currentTime);
        src.connect(gain);
        gain.connect(this.ctx.destination);
        src.start(0);
        return;
      } catch (e) {
        console.warn("Buffer playback fallback:", e);
      }
    }

    // Fallback to synthetic if buffer isn't loaded yet
    if (fallbackFn) fallbackFn();
  }

  playRelayClick() {
    this.playBuffer('click', () => this._syntheticRelay());
  }

  playSwitchSnap() {
    this.playBuffer('toggle', () => this._syntheticSnap());
  }

  playTabSwitch() {
    this.playBuffer('tab', () => this._syntheticRelay());
  }

  playLaunchSiren() {
    this.playBuffer('launch', () => this._syntheticLaunch());
  }

  // Fallback WebAudio synthesisers
  _syntheticRelay() {
    if (!this.ctx) return;
    const t = this.ctx.currentTime;
    const osc = this.ctx.createOscillator();
    const gain = this.ctx.createGain();
    osc.type = 'triangle';
    osc.frequency.setValueAtTime(1200, t);
    osc.frequency.exponentialRampToValueAtTime(150, t + 0.035);
    gain.gain.setValueAtTime(0.25, t);
    gain.gain.exponentialRampToValueAtTime(0.001, t + 0.035);
    osc.connect(gain);
    gain.connect(this.ctx.destination);
    osc.start(t);
    osc.stop(t + 0.04);
  }

  _syntheticSnap() {
    if (!this.ctx) return;
    const t = this.ctx.currentTime;
    const osc = this.ctx.createOscillator();
    const gain = this.ctx.createGain();
    osc.type = 'square';
    osc.frequency.setValueAtTime(450, t);
    osc.frequency.exponentialRampToValueAtTime(80, t + 0.05);
    gain.gain.setValueAtTime(0.3, t);
    gain.gain.exponentialRampToValueAtTime(0.001, t + 0.05);
    osc.connect(gain);
    gain.connect(this.ctx.destination);
    osc.start(t);
    osc.stop(t + 0.055);
  }

  _syntheticLaunch() {
    if (!this.ctx) return;
    const t = this.ctx.currentTime;
    const osc = this.ctx.createOscillator();
    const gain = this.ctx.createGain();
    osc.type = 'sawtooth';
    osc.frequency.setValueAtTime(320, t);
    osc.frequency.linearRampToValueAtTime(880, t + 0.18);
    osc.frequency.exponentialRampToValueAtTime(200, t + 0.45);
    gain.gain.setValueAtTime(0.2, t);
    gain.gain.exponentialRampToValueAtTime(0.001, t + 0.45);
    osc.connect(gain);
    gain.connect(this.ctx.destination);
    osc.start(t);
    osc.stop(t + 0.46);
  }

  toggleSound() {
    this.enabled = !this.enabled;
    return this.enabled;
  }
}

// Global singleton instance
window.pipAudio = new PipBoyAudioEngine();

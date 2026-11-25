/**
 * Lightweight Wasteland Embers & Radioactive Ash particle engine.
 * Throttled to 24 FPS, pauses when hidden, and avoids expensive Canvas shadowBlur for low-end PCs.
 */
class WastelandParticles {
  constructor(canvasId) {
    this.canvas = document.getElementById(canvasId);
    if (!this.canvas) return;
    this.ctx = this.canvas.getContext('2d', { alpha: true });
    this.particles = [];
    this.particleCount = 24;
    this.width = window.innerWidth;
    this.height = window.innerHeight;
    this.lastFrame = 0;
    this.frameInterval = 1000 / 24; // 24 FPS cap for minimal CPU/GPU load
    this.isPaused = document.hidden;

    this.resize();
    window.addEventListener('resize', () => this.resize());
    document.addEventListener('visibilitychange', () => {
      this.isPaused = document.hidden;
    });

    this.initParticles();
    requestAnimationFrame((ts) => this.animate(ts));
  }

  resize() {
    this.width = window.innerWidth;
    this.height = window.innerHeight;
    this.canvas.width = this.width;
    this.canvas.height = this.height;
  }

  initParticles() {
    this.particles = [];
    for (let i = 0; i < this.particleCount; i++) {
      this.particles.push({
        x: Math.random() * this.width,
        y: Math.random() * this.height,
        size: Math.random() * 2.0 + 0.8,
        speedX: (Math.random() - 0.4) * 0.65,
        speedY: -(Math.random() * 0.85 + 0.3),
        opacity: Math.random() * 0.65 + 0.2,
        color: Math.random() > 0.8 ? '255, 176, 0' : '0, 255, 102'
      });
    }
  }

  animate(timestamp) {
    requestAnimationFrame((ts) => this.animate(ts));

    if (this.isPaused) return;
    if (timestamp - this.lastFrame < this.frameInterval) return;
    this.lastFrame = timestamp;

    this.ctx.clearRect(0, 0, this.width, this.height);

    for (let i = 0; i < this.particles.length; i++) {
      const p = this.particles[i];

      p.x += p.speedX;
      p.y += p.speedY;

      if (p.y < -10) {
        p.y = this.height + 10;
        p.x = Math.random() * this.width;
      }
      if (p.x < -10) p.x = this.width + 10;
      if (p.x > this.width + 10) p.x = -10;

      // Soft outer halo without expensive shadowBlur
      this.ctx.fillStyle = `rgba(${p.color}, ${p.opacity * 0.25})`;
      this.ctx.beginPath();
      this.ctx.arc(p.x, p.y, p.size * 2.2, 0, Math.PI * 2);
      this.ctx.fill();

      // Bright core
      this.ctx.fillStyle = `rgba(${p.color}, ${p.opacity})`;
      this.ctx.beginPath();
      this.ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
      this.ctx.fill();
    }
  }
}

document.addEventListener('DOMContentLoaded', () => {
  new WastelandParticles('particles-canvas');
});

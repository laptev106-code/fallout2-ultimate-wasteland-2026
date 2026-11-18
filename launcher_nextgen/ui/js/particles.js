/**
 * Hardware-accelerated Wasteland Embers & Radioactive Ash particle engine.
 * Runs smoothly on 60-144 Hz monitors using requestAnimationFrame.
 */
class WastelandParticles {
  constructor(canvasId) {
    this.canvas = document.getElementById(canvasId);
    if (!this.canvas) return;
    this.ctx = this.canvas.getContext('2d');
    this.particles = [];
    this.particleCount = 55;
    this.width = window.innerWidth;
    this.height = window.innerHeight;
    
    this.resize();
    window.addEventListener('resize', () => this.resize());
    this.initParticles();
    this.animate();
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
        size: Math.random() * 2.2 + 0.6,
        speedX: (Math.random() - 0.4) * 0.4,
        speedY: -(Math.random() * 0.6 + 0.2),
        opacity: Math.random() * 0.7 + 0.2,
        color: Math.random() > 0.8 ? '255, 176, 0' : '0, 255, 102' // Occasional amber ember among green phosphor ash
      });
    }
  }

  animate() {
    this.ctx.clearRect(0, 0, this.width, this.height);

    for (let i = 0; i < this.particles.length; i++) {
      const p = this.particles[i];

      p.x += p.speedX;
      p.y += p.speedY;

      // Wrap around screen
      if (p.y < -10) {
        p.y = this.height + 10;
        p.x = Math.random() * this.width;
      }
      if (p.x < -10) p.x = this.width + 10;
      if (p.x > this.width + 10) p.x = -10;

      this.ctx.beginPath();
      this.ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
      this.ctx.fillStyle = `rgba(${p.color}, ${p.opacity})`;
      this.ctx.shadowBlur = p.size * 2;
      this.ctx.shadowColor = `rgba(${p.color}, 0.5)`;
      this.ctx.fill();
    }

    requestAnimationFrame(() => this.animate());
  }
}

document.addEventListener('DOMContentLoaded', () => {
  new WastelandParticles('particles-canvas');
});

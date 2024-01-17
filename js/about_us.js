document.addEventListener('DOMContentLoaded', function() {
    const canvas = document.getElementById('network');
    const ctx = canvas.getContext('2d');
    
    // Set canvas size to full window size
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    class Particle {
        constructor() {
            this.radius = Math.random() * 2 + 1.5;
            this.x = Math.random() * canvas.width;
            this.y = Math.random() * canvas.height;
            this.speedX = (Math.random() - 0.5) * 0.5;
            this.speedY = (Math.random() - 0.5) * 0.5;
        }

        update() {
            if (this.x + this.radius > canvas.width || this.x - this.radius < 0) {
                this.speedX = -this.speedX;
            }
            if (this.y + this.radius > canvas.height || this.y - this.radius < 0) {
                this.speedY = -this.speedY;
            }
            this.x += this.speedX;
            this.y += this.speedY;
        }

        draw() {
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
            ctx.fillStyle = 'rgba(0,0,0,0.7)';
            ctx.fill();
        }
    }

    let particlesArray = [];
    const numberOfParticles = 150;

    function init() {
        particlesArray = [];
        for (let i = 0; i < numberOfParticles; i++) {
            particlesArray.push(new Particle());
        }
    }

    function animate() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        for (let i = 0; i < particlesArray.length; i++) {
            particlesArray[i].update();
            particlesArray[i].draw();
        }
        connect();
        requestAnimationFrame(animate);
    }

    function connect() {
        let maxDistance = 100;
        for (let i = 0; i < particlesArray.length; i++) {
            for (let j = i + 1; j < particlesArray.length; j++) {
                let dx = particlesArray[i].x - particlesArray[j].x;
                let dy = particlesArray[i].y - particlesArray[j].y;
                let distance = Math.sqrt(dx * dx + dy * dy);

                if (distance < maxDistance) {
                    ctx.strokeStyle = 'rgba(0,0,0,' + (1 - distance / maxDistance) + ')';
                    ctx.lineWidth = 1;
                    ctx.beginPath();
                    ctx.moveTo(particlesArray[i].x, particlesArray[i].y);
                    ctx.lineTo(particlesArray[j].x, particlesArray[j].y);
                    ctx.stroke();
                }
            }
        }
    }

    init();
    animate();

});
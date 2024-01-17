document.addEventListener('DOMContentLoaded', function() {
    const canvas = document.getElementById('particle-network');
    const ctx = canvas.getContext('2d');
    canvas.width = document.getElementById('main-circle').offsetWidth;
    canvas.height = document.getElementById('main-circle').offsetHeight;

    class Particle {
        constructor() {
            this.radius = Math.random() * 1.5 + 1.5; // Smaller size
            const maxDistanceFromCenter = canvas.width / 2; // Adjust as needed
            const angle = Math.random() * Math.PI * 2;
            const distance = Math.random() * maxDistanceFromCenter;
    
            this.x = canvas.width / 2 + Math.cos(angle) * distance;
            this.y = canvas.height / 2 + Math.sin(angle) * distance;
            this.speedX = (Math.random() - 0.5) * 0.25; // Slower movement
            this.speedY = (Math.random() - 0.5) * 0.25; // Slower movement
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
    const numberOfParticles = 80; // Adjust the number of particles here

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
        let maxDistance = 65; // Max distance for line connection, adjust as needed
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

    const numCircles = 5;
    const mainCircle = document.getElementById('main-circle');
    const outerCircles = document.querySelectorAll('.outer-circle');

    const mainRadius = mainCircle.offsetWidth / 1.75;
    const distanceFromCenter = mainRadius + 35; // Adjust as needed

    outerCircles.forEach((circle, index) => {
        const angle = (2 * Math.PI / numCircles) * index;
        const x = Math.cos(angle) * distanceFromCenter;
        const y = Math.sin(angle) * distanceFromCenter;

        circle.style.transform = `translate(${x}px, ${y}px)`;
    });

    document.querySelectorAll('.outer-circle').forEach(circle => {
        circle.addEventListener('click', () => {
            window.location.href = circle.getAttribute('data-link');
        });
    });
});
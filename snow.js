const canvas = document.getElementById("snow");
const ctx = canvas.getContext("2d");

canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

window.addEventListener("resize", () => {
	canvas.width = window.innerWidth;
	canvas.height = window.innerHeight;
	initSnow();
});

let snowflakes = [];
let snowPile = [];
const snowAmount = 150;

function initSnow() {
	snowflakes = [];
	snowPile = new Array(canvas.width).fill(0);

	for (let i = 0; i < snowAmount; i++) {
		snowflakes.push(createFlake());
	}
}

function createFlake() {
	return {
		x: Math.random() * canvas.width,
		y: Math.random() * canvas.height,
		radius: Math.random() * 3 + 1,
		speed: Math.random() * 1 + 0.5
	};
}

function draw() {
	ctx.clearRect(0, 0, canvas.width, canvas.height);

	// Draw pile
	ctx.fillStyle = "white";
	ctx.beginPath();
	ctx.moveTo(0, canvas.height);

	for (let x = 0; x < canvas.width; x++) {
		ctx.lineTo(x, canvas.height - snowPile[x]);
	}

	ctx.lineTo(canvas.width, canvas.height);
	ctx.closePath();
	ctx.fill();

	// Draw flakes
	for (let flake of snowflakes) {
		ctx.beginPath();
		ctx.arc(flake.x, flake.y, flake.radius, 0, Math.PI * 2);
		ctx.fill();

		flake.y += flake.speed;

		const groundHeight = snowPile[Math.floor(flake.x)];

		if (flake.y + flake.radius >= canvas.height - groundHeight) {
			snowPile[Math.floor(flake.x)] += flake.radius;
			Object.assign(flake, createFlake());
			flake.y = 0;
		}
	}

	requestAnimationFrame(draw);
}

initSnow();
draw();

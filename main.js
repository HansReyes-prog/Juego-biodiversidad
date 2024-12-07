// Configuración del Canvas y contexto
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

// Constantes
const ANCHO = 800;
const ALTO = 600;
const VELOCIDAD = 5;
const COLOR_FONDO = "#121212";
const PUNTOS_GANAR = 100;

// Rutas de imágenes (reemplaza con tus sprites)
const URL_PERSONAJE = "https://via.placeholder.com/40x40.png?text=P";
const URL_ENEMIGO = "https://via.placeholder.com/30x30.png?text=E";

// Cargar imágenes
const imgPersonaje = new Image();
imgPersonaje.src = URL_PERSONAJE;

const imgEnemigo = new Image();
imgEnemigo.src = URL_ENEMIGO;

// Clase Personaje
class Personaje {
    constructor(x, y) {
        this.x = x;
        this.y = y;
        this.w = 40;
        this.h = 40;
        this.vel = VELOCIDAD;
    }

    mover(keys) {
        if (keys['ArrowUp']) this.y -= this.vel;
        if (keys['ArrowDown']) this.y += this.vel;
        if (keys['ArrowLeft']) this.x -= this.vel;
        if (keys['ArrowRight']) this.x += this.vel;
    }

    dibujar() {
        ctx.drawImage(imgPersonaje, this.x, this.y, this.w, this.h);
    }
}

// Clase Enemigo
class Enemigo {
    constructor(x, y) {
        this.x = x;
        this.y = y;
        this.w = 30;
        this.h = 30;
    }

    dibujar() {
        ctx.drawImage(imgEnemigo, this.x, this.y, this.w, this.h);
    }

    colisiona(jugador) {
        return (
            this.x < jugador.x + jugador.w &&
            this.x + this.w > jugador.x &&
            this.y < jugador.y + jugador.h &&
            this.y + this.h > jugador.y
        );
    }
}

// Variables del juego
const jugador = new Personaje(100, 100);
const enemigos = [
    new Enemigo(400, 300),
    new Enemigo(200, 500)
];
let puntuacion = 0;
const keys = {};

// Actualizar puntuación
function actualizarPuntuacion() {
    document.getElementById('score').innerText = `Puntuación: ${puntuacion}`;
}

// Dibujar fondo
function dibujarFondo() {
    ctx.fillStyle = COLOR_FONDO;
    ctx.fillRect(0, 0, ANCHO, ALTO);
}

// Bucle del juego
function loop() {
    // Limpiar canvas
    dibujarFondo();

    // Mover y dibujar jugador
    jugador.mover(keys);
    jugador.dibujar();

    // Dibujar enemigos y verificar colisiones
    enemigos.forEach((enemigo, index) => {
        enemigo.dibujar();
        if (enemigo.colisiona(jugador)) {
            enemigos.splice(index, 1); // Eliminar enemigo
            puntuacion += 10;
            actualizarPuntuacion();
        }
    });

    // Verificar si el jugador ha ganado
    if (puntuacion >= PUNTOS_GANAR) {
        alert("¡Has ganado!");
        window.location.reload();
    }

    // Continuar el bucle
    requestAnimationFrame(loop);
}

// Event listeners para teclas
window.addEventListener('keydown', (e) => keys[e.key] = true);
window.addEventListener('keyup', (e) => keys[e.key] = false);

// Iniciar el juego
loop();

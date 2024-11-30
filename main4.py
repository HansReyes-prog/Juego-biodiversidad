# Ejemplo de árbol de decisiones para diálogos
dialogos = {
    "inicio": {
        "pregunta": "¿Qué deseas hacer?",
        "opciones": {
            "explorar": "Explora el mundo a tu alrededor.",
            "hablar": {
                "pregunta": "¿Con quién deseas hablar?",
                "opciones": {
                    "NPC1": "El NPC1 te habla sobre la historia local.",
                    "NPC2": "El NPC2 te da una pista para tu misión."
                }
            }
        }
    }
}


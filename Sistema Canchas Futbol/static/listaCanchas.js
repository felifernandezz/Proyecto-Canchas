import axios from "axios";

document.addEventListener("DOMContentLoaded", () => {
    const canchaList = document.getElementById("cancha-list");

    // 1. Obtener y renderizar la lista de canchas
    const fetchCanchas = async () => {
        try {
            const response = await axios.get("/api/canchas");
            renderCanchas(response.data);
        } catch (error) {
            console.error("Error al obtener las canchas:", error);
        }
    };

    const renderCanchas = (canchas) => {
        canchaList.innerHTML = ""; // Limpia la lista
        canchas.forEach((cancha) => {
            const li = document.createElement("li");
            li.textContent = `${cancha.tipo_cancha} - Cantidad: ${cancha.cantidad}`;
            li.classList.add("cancha-item"); // Clase para identificar los elementos
            li.dataset.canchaId = cancha.id; // Agrega un atributo con el ID de la cancha
            canchaList.appendChild(li);
        });

        // Agregar eventos de clic para redirigir al calendario
        const canchaItems = document.querySelectorAll(".cancha-item");
        canchaItems.forEach((item) => {
            item.addEventListener("click", () => {
                const canchaId = item.dataset.canchaId; // Obtener el ID de la cancha
                // Redirigir al calendario, pasando el ID de la cancha como parámetro
                window.location.href = `/reserva?cancha_id=${canchaId}`;
            });
        });
    };

    fetchCanchas();
});

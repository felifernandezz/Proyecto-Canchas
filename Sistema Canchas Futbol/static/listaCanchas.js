import axios from "axios";

document.addEventListener("DOMContentLoaded", () => {
    const canchaList = document.getElementById("cancha-list");

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
            canchaList.appendChild(li);
        });
    };

    fetchCanchas();
});

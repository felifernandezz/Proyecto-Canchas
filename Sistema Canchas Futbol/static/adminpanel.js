import axios from "axios";

// Esta función obtiene el token de autenticación del almacenamiento local o de los headers
const obtenerToken = () => localStorage.getItem("jwt_token");

document.addEventListener("DOMContentLoaded", () => {
    const canchaList = document.getElementById("cancha-list");
    const form = document.getElementById("admin-form");

    // Verifica si el usuario es administrador antes de permitir el acceso
    const verificarAccesoAdmin = async () => {
        try {
            const token = obtenerToken();
            const response = await axios.get("/api/verificar-admin", {
                headers: { Authorization: `Bearer ${token}` },
            });
            // Si el usuario es admin, continúa con el flujo normal
            if (response.data.rol !== "admin") {
                window.location.href = "/"; // Redirige si no es admin
            } else {
                fetchCanchas(); // Obtiene las canchas solo si es admin
            }
        } catch (error) {
            console.error("Error de verificación de acceso:", error);
            window.location.href = "/"; // Redirige si hay error
        }
    };

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
            const editBtn = document.createElement("button");
            editBtn.textContent = "Editar";
            editBtn.addEventListener("click", () => populateForm(cancha));
            const deleteBtn = document.createElement("button");
            deleteBtn.textContent = "Eliminar";
            deleteBtn.addEventListener("click", () => deleteCancha(cancha.id));
            li.append(editBtn, deleteBtn);
            canchaList.appendChild(li);
        });
    };

    const populateForm = (cancha) => {
        form["tipo_cancha"].value = cancha.tipo_cancha;
        form["cantidad"].value = cancha.cantidad;
        form["id"].value = cancha.id;
    };

    const saveCancha = async (e) => {
        e.preventDefault();
        const cancha = {
            id: form["id"].value || null,
            tipo_cancha: form["tipo_cancha"].value,
            cantidad: form["cantidad"].value,
        };

        try {
            if (cancha.id) {
                await axios.put(`/api/canchas/${cancha.id}`, cancha);
            } else {
                await axios.post("/api/canchas", cancha);
            }
            fetchCanchas();
            form.reset();
        } catch (error) {
            console.error("Error al guardar cancha:", error);
        }
    };

    const deleteCancha = async (id) => {
        try {
            await axios.delete(`/api/canchas/${id}`);
            fetchCanchas();
        } catch (error) {
            console.error("Error al eliminar cancha:", error);
        }
    };

    form.addEventListener("submit", saveCancha);
    verificarAccesoAdmin(); // Verifica el acceso al panel
});

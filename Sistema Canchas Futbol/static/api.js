import axios from "axios";

// Función para editar una cancha
export const editCancha = async (id, data) => {
    try {
        const response = await axios.put(`/api/canchas/${id}`, data); // Envía la solicitud PUT
        return response.data; // Devuelve los datos de la cancha actualizada
    } catch (error) {
        console.error("Error al editar la cancha", error);
    }
};

// Función para eliminar una cancha
export const deleteCancha = async (id) => {
    try {
        const response = await axios.delete(`/api/canchas/${id}`); // Envía la solicitud DELETE
        return response.data; // Devuelve el estado de la eliminación
    } catch (error) {
        console.error("Error al eliminar la cancha", error);
    }
};

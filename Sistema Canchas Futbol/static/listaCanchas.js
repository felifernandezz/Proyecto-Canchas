import axios from "axios";
import { useState, useEffect } from "react";

// Función para obtener las canchas
const fetchCanchas = async () => {
    try {
        const response = await axios.get("http://127.0.0.1:5000/canchas"); // Cambia la URL según el endpoint real
        console.log(response.data); // Verifica que obtienes los datos del backend
    } catch (error) {
        console.error("Error al obtener las canchas:", error);
    }
};

fetchCanchas();

// Componente para mostrar las canchas
const CanchasList = () => {
    const [canchas, setCanchas] = useState([]);

    useEffect(() => {
        axios.get("http://127.0.0.1:5000/canchas") // Cambia la URL según el endpoint real
            .then(response => setCanchas(response.data))
            .catch(error => console.error(error));
    }, []);

    return (
        <div>
            <h1>Lista de Canchas</h1>
            <ul>
                {canchas.map(c => (
                    <li key={c.id}>{c.tipo_cancha} - ${c.precio}</li> // Renderiza el tipo y precio de la cancha
                ))}
            </ul>
        </div>
    );
};

export default CanchasList;

import React, { useState, useEffect } from "react";
import axios from "axios";
import { editCancha, deleteCancha } from "./api"; // Importa las funciones de api.js

const AdminPanel = () => {
    const [canchas, setCanchas] = useState([]);
    const [form, setForm] = useState({ id: null, tipo_cancha: "", cantidad: "", precio: "" });

    // Obtiene la lista de canchas del servidor
    useEffect(() => {
        fetchCanchas();
    }, []);

    // Función para obtener canchas del backend
    const fetchCanchas = async () => {
        try {
            const response = await axios.get("http://127.0.0.1:5000/tipos"); // Cambia la URL según el endpoint real
            setCanchas(response.data);
        } catch (error) {
            console.error("Error al obtener canchas:", error);
        }
    };

    // Función para manejar la edición de una cancha
    const handleEdit = (cancha) => {
        setForm(cancha); // Rellena el formulario con los datos de la cancha seleccionada
    };

    // Función para manejar la eliminación de una cancha
    const handleDelete = async (id) => {
        try {
            await deleteCancha(id); // Llama a la función deleteCancha desde api.js
            fetchCanchas(); // Vuelve a obtener la lista de canchas después de eliminar
        } catch (error) {
            console.error("Error al eliminar cancha:", error);
        }
    };

    // Función para guardar una nueva cancha o actualizar una existente
    const handleSave = async () => {
        try {
            if (form.id) {
                await editCancha(form.id, form); // Llama a la función editCancha desde api.js para actualizar
            }
            setForm({ id: null, tipo_cancha: "", cantidad: "", precio: "" }); // Reinicia el formulario
            fetchCanchas(); // Vuelve a obtener la lista de canchas
        } catch (error) {
            console.error("Error al guardar cancha:", error);
        }
    };

    return (
        <div>
            <h1>Panel de Administración</h1>
            <form onSubmit={(e) => { e.preventDefault(); handleSave(); }}>
                <input
                    type="text"
                    placeholder="Tipo de cancha"
                    value={form.tipo_cancha}
                    onChange={(e) => setForm({ ...form, tipo_cancha: e.target.value })}
                />
                <input
                    type="number"
                    placeholder="Cantidad"
                    value={form.cantidad}
                    onChange={(e) => setForm({ ...form, cantidad: e.target.value })}
                />
                <input
                    type="number"
                    placeholder="Precio"
                    value={form.precio}
                    onChange={(e) => setForm({ ...form, precio: e.target.value })}
                />
                <button type="submit">{form.id ? "Actualizar" : "Agregar"}</button>
            </form>
            <ul>
                {canchas.map((c) => (
                    <li key={c.id}>
                        {c.tipo_cancha} - {c.cantidad} - ${c.precio}{" "}
                        <button onClick={() => handleEdit(c)}>Editar</button>
                        <button onClick={() => handleDelete(c.id)}>Eliminar</button>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default AdminPanel;

import axios from "axios";

export const fetchCanchas = async () => {
    return await axios.get("/api/canchas");
};

export const saveCancha = async (data) => {
    if (data.id) {
        return await axios.put(`/api/canchas/${data.id}`, data);
    } else {
        return await axios.post("/api/canchas", data);
    }
};

export const deleteCancha = async (id) => {
    return await axios.delete(`/api/canchas/${id}`);
};

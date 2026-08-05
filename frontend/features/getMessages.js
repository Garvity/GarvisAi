import api from "../utils/axios.js";

const getMessages = async (id) => {
    try{
        const { data } = await api.get(`/api/chat/get-messages/${id}`);
        return data;
    }catch(err){
        console.error(err.response);
        console.error(err.response?.data);
        console.error(err.message);
        return [];
    }
}

export default getMessages;
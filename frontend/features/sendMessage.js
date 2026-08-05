import api from "../utils/axios.js";

const sendMessage = async (payload) => {
    try{
        const { data } = await api.post('/api/agent/chat', payload);
        return data;
    }catch(err){
        // console.error("sendMessage error",err)
        console.error("Status:", err.response?.status);
        console.error("Response:", err.response?.data);
        console.error(err);
        return null;
    }
}

export default sendMessage;
import api from "../utils/axios.js";

const updateConversation = async (payload) => {
    try{
        const { data } = await api.post('/api/chat/update-conversation', payload);
        return data;
    }catch(err){
        // console.error("sendMessage error",err)
        console.error("Status:", err.response?.status);
        console.error("Response:", err.response?.data);
        console.error(err);
        return [];
    }
}

export default updateConversation;
import api from "../utils/axios.js";

export const getConversations = async () => {
    try{
        const {data} = await api.get("/api/chat/get-conversations");
        console.log("getConversation data",data)
        return data;
    }catch(err){
        console.error("Error getting conversation:", err);
        return []
    }
}
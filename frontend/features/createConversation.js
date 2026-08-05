import api from "../utils/axios.js";

export const createConversation = async () => {
    try{
        const {data} = await api.get("/api/chat/create-conversation");
        console.log("createConversation data",data)
        return data;
    }catch(err){
        console.error("Error creating conversation:", err);
        return []
    }
}
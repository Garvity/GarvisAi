import api from "../utils/axios.js";

const getCurrentUser = async () => {
    try{
        const { data } = await api.get("/api/me");
        return data;
    }catch(err){
        console.error("getCurrentUser error",err)
        return null;
    }
}

export default getCurrentUser;
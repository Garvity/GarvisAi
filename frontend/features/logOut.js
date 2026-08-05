import api from "../utils/axios.js";

export const logOut = async () => {
    try{
        const {data} = await api.get("/api/auth/logout");
        console.log("logOut data",data)
    }catch(err){
        console.error("Error logging out:", err);
    }
}
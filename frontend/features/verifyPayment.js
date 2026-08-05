import api from "../utils/axios.js";

export const verifyPayment = async (payload) => {
    try{
        const {data} = await api.post("/api/billing/verify-payment", payload);
        console.log("verifyPayment data",data)
        return data;
    }catch(err){
        console.error("Error verifying payment:", err);
        return []
    }
}
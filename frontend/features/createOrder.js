import api from "../utils/axios.js";

export const createOrder = async (plan) => {
    try{
        const {data} = await api.post("/api/billing/create-order", {plan});
        console.log("createOrder data",data)
        return data;
    }catch(err){
        console.error("Error creating order:", err);
        return []
    }
}
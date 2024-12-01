import axios from 'axios';

const API_URL = "http://10.49.12.59:1337"

export const GetPrediction = async (file) => {
    const formData = new FormData();
    formData.append("file", file);

    try {
        const response = await axios.post(
            `${API_URL}/api/predict/sign`, 
            formData, 
            {
                headers: {
                    "Content-Type": "multipart/form-data",
                },
            }
        );
        console.log(response)
        console.log("this is response data: ", response.data)
        if(response.status == 200) {
            return response.data;
        }
    } catch (error) {
        console.error("Error uploading file:", error);
        throw error;
    }
};

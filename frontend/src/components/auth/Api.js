import axios from 'axios';

class HandleApiCalls {
    Register(username, email, password, first_name, last_name) {

        if (username && email && password && first_name && last_name) {
            return axios.post('http://127.0.0.1:8000/api/register/', {
                username,
                email,
                password,
                first_name,
                last_name
            }).then((res) => {
                console.log("Registered:", res.data);
                return res.data;
            }).catch((err) => {
                console.error("Login error:", err.response?.data || err.message);
            });
        } else {
            console.log("All fields should be filled");
        }

    }


    Login(email, password) {
        return axios.post('http://127.0.0.1:8000/api/login/', {
            email,
            password,
        }).then((res) => {
            console.log("Login successful:", res.data);
            return res.data;
        }).catch((err) => {
            console.error("Login error:", err.response?.data || err.message);
        });
    }
    VerifyEmail(uid, token) {
        return axios.post('http://127.0.0.1:8000/api/emailverification/', {
            uid,
            token
        });
    }
    deleteInactiveUser() {
        return axios.post('http://127.0.0.1:8000/api/deleteinactiveuser/', {


        }).then((res) => {
            console.log(res.data);
        });
    }

}


export default HandleApiCalls;
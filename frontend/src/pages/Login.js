import React from "react";
import { useMsal } from "@azure/msal-react";
import { loginRequest } from "../authConfig";
import { useNavigate } from "react-router-dom"; 

const Login = () => {
    const { instance } = useMsal();
    const navigate = useNavigate(); 

    const handleLogin = () => {
        instance.loginPopup(loginRequest)
            .then(response => {
                navigate("/dashboard"); 
            })
            .catch(error => console.error("Login error", error));
    };

    return (
        <div className="login-container">
            <h2>Welcome to the App</h2>
            <button onClick={handleLogin}>Login with Azure AD</button>
        </div>
    );
};

export default Login;

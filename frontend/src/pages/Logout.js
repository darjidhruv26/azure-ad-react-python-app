import React from "react";
import { useMsal } from "@azure/msal-react";
import { useNavigate } from "react-router-dom";

const Logout = () => {
    const { instance } = useMsal();
    const navigate = useNavigate();

    const handleLogout = async () => {
        try {
            await instance.logoutPopup(); // Logout using popup
            console.log("Logout successful");

            // Clear stored credentials
            sessionStorage.clear();
            localStorage.clear();

            // Redirect to login page
            navigate("/");
        } catch (error) {
            console.error("Logout Error:", error);
        }
    };

    return <button onClick={handleLogout}>Logout</button>;
};

export default Logout;

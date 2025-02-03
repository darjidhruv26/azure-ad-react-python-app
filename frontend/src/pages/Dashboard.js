import React, { useEffect, useState } from "react";
import axios from "axios";
import { useMsal } from "@azure/msal-react";
import { loginRequest } from "../authConfig";
import { useNavigate } from "react-router-dom";
import Logout from "./Logout"; 

const Dashboard = () => {
    const { instance, accounts } = useMsal(); 
    const navigate = useNavigate();
    const [userData, setUserData] = useState(null);

    useEffect(() => {
        const storedAccount = JSON.parse(localStorage.getItem("activeAccount"));
        const accountToUse = accounts.length > 0 ? accounts[0] : storedAccount;

        if (accountToUse) {
            instance.setActiveAccount(accountToUse);
            localStorage.setItem("activeAccount", JSON.stringify(accountToUse));

            const cachedToken = sessionStorage.getItem("accessToken");

            if (cachedToken) {
                fetchDashboardData(cachedToken);
            } else {
                instance.acquireTokenSilent({
                    ...loginRequest,
                    account: accountToUse, 
                }).then(tokenResponse => {
                    sessionStorage.setItem("accessToken", tokenResponse.accessToken);
                    fetchDashboardData(tokenResponse.accessToken);
                }).catch(error => {
                    console.error("Token Error:", error);
                    navigate("/"); 
                });
            }
        } else {
            navigate("/"); 
        }
    }, [instance, accounts, navigate]);

    const fetchDashboardData = (token) => {
        const apiBaseUrl = process.env.REACT_APP_API_BASE_URL;
        axios.get(`${apiBaseUrl}api/v1/dashboard/`, {
            headers: { Authorization: `Bearer ${token}` },
        }).then(response => {
            setUserData(response.data);
        }).catch(error => console.error("API Error:", error));
    };

    const handleLogout = () => {
        localStorage.removeItem("activeAccount");
        sessionStorage.removeItem("accessToken");
        instance.logoutRedirect().then(() => {
            navigate("/");
        });
    };

    return (
        <div>
            <h2>Dashboard</h2>
            {userData ? (
                <>
                    <p><strong>Username:</strong> {userData.username}</p>
                    <p><strong>Email:</strong> {userData.email || "Not Available"}</p>
                    <p><strong>Full Name:</strong> {userData.full_name || "Not Available"}</p>
                    <p>{userData.message}</p>
                </>
            ) : (
                <p>Loading user details...</p>
            )}
            <Logout onLogout={handleLogout} />
        </div>
    );
};

export default Dashboard;

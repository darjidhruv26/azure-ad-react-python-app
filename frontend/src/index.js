import React from "react";
import { createRoot } from "react-dom/client"; 
import { PublicClientApplication } from "@azure/msal-browser";
import { MsalProvider } from "@azure/msal-react";
import { msalConfig } from "./authConfig";
import App from "./App";

const msalInstance = new PublicClientApplication(msalConfig);

const container = document.getElementById("root");
const root = createRoot(container); 

root.render(
    <MsalProvider instance={msalInstance}>
        <App />
    </MsalProvider>
);
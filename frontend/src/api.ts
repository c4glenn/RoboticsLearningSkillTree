import axios from "axios";

const API_BASE_URL = "http://localhost:8000/api";

const api = axios.create({
    baseURL: API_BASE_URL,
});

let accessToken = localStorage.getItem("accessToken");

api.interceptors.request.use((config) => {
    if (accessToken) {
        config.headers.Authorization = `Bearer ${accessToken}`;
    }
    return config;
});

export async function login(username: string, password: string) {
    try {
        const response = await api.post("/auth/token/", { username, password });
        accessToken = response.data.access;
        if (!accessToken) {
            throw new Error("No access token received");
        }
        localStorage.setItem("accessToken", accessToken);
        localStorage.setItem("refresh_token", response.data.refresh);
        return response.data;
    } catch (error) {
        console.error("Login failed:", error);
        throw error;
    }
}

export async function logout() {
    const refreshToken = localStorage.getItem("refresh_token");
    if (!refreshToken) {
        throw new Error("No refresh token found");
    }
    try {
        await api.post("/accounts/logout/", { refresh: refreshToken });
        localStorage.removeItem("accessToken");
        localStorage.removeItem("refresh_token");
        accessToken = null;
    } catch (error) {
        console.error("Logout failed:", error);
        throw error;
    }
}

export async function refreshToken() {
    const refreshToken = localStorage.getItem("refresh_token");
    if (!refreshToken) {
        throw new Error("No refresh token found");
    }
    try {
        const response = await api.post("/auth/token/refresh/", { refresh: refreshToken });
        accessToken = response.data.access;
        if (!accessToken) {
            throw new Error("No access token received on refresh");
        }
        localStorage.setItem("accessToken", accessToken);
        return accessToken;
    } catch (error) {
        console.error("Token refresh failed:", error);
        throw error;
    }
}

export default api;
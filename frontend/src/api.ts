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
        api.defaults.headers.common['Authorization'] = `Bearer ${accessToken}`;
        localStorage.setItem("accessToken", accessToken);
        localStorage.setItem("refresh_token", response.data.refresh);

        return response.data;
    } catch (error) {
        console.error("Login failed:", error);
        throw error;
    }
}

export async function register(username: string, email: string, password: string, firstName?: string, lastName?: string) {
    try {
        const response = await api.post("/accounts/register/", {username, email, password, firstName, lastName});
        return response.data;
    } catch (error: any) {
        if (error.response) {
            console.error("Registration failed:", error.response.data);
        } else {
            console.error("Registration failed:", error.message);
        }
        throw error;
    }
}

export async function getUserProfile() {
    if (!accessToken) {
        throw new Error("User is not authenticated");
    }
    try {
        const response = await api.get("/accounts/me/");
        return response.data;
    } catch (error) {
        console.error("Failed to fetch user profile:", error);
        throw error;
    }
}

export async function logout() {
    const refreshToken = localStorage.getItem("refresh_token");
    if (!refreshToken) {
        throw new Error("No refresh token found");
    }
    try {
        console.log("Logging out with refresh token:", refreshToken);
        await api.post("/accounts/logout/", { refresh: refreshToken }, {
            headers: {
                Authorization: `Bearer ${accessToken}`,
            },
        });
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

let isRefreshing = false;
let requestQueue: {
    resolve: (value?: any) => void;
    reject: (reason?: any) => void;
}[] = [];


function processQueue(error: any, newToken: string | null) {
    requestQueue.forEach((prom) => {
        if (newToken) {
            prom.resolve(newToken);
        }
        else {
            prom.reject(error);
        }
    });
    requestQueue = [];
}

api.interceptors.response.use(
    (response) => response,
    async (error) => {
        const originalRequest = error.config;

        if (error.response?.status === 401 && !originalRequest._retry) {
            if (isRefreshing) {
                return new Promise((resolve, reject) => {
                    requestQueue.push({
                        resolve: (token: string) => {
                                originalRequest.headers['Authorization'] = `Bearer ${token}`;
                                resolve(api(originalRequest));
                        },
                        reject,
                    });
                });
            }
            originalRequest._retry = true;
            isRefreshing = true;
            try {
                const newToken = await refreshToken();
                accessToken = newToken;
                api.defaults.headers.common['Authorization'] = `Bearer ${newToken}`;
                processQueue(null, newToken);
                originalRequest.headers['Authorization'] = `Bearer ${newToken}`;
                return api(originalRequest);
            } catch (err) {
                processQueue(err, null);
                localStorage.removeItem("accessToken");
                localStorage.removeItem("refresh_token");
                return Promise.reject(err);

            } finally {
                isRefreshing = false;
            }
        }
    }
);


export default api;
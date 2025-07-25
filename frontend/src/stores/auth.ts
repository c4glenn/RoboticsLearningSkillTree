import { defineStore } from "pinia";
import { login, logout, refreshToken, getUserProfile } from "@/api";
import router from "@/router";

export const useAuthStore = defineStore("auth", {
    state: () => ({
        user: null as null | { username: string; email: string },
        accessToken: localStorage.getItem("accessToken") || null as string | null,
        refreshToken: localStorage.getItem("refresh_token") || null as string | null,
        isAuthenticated: !!localStorage.getItem("accessToken"),
    }),
    actions: {
        async fetchUserProfile() {
            if (!this.accessToken) {
                throw new Error("User is not authenticated");
            }
            try {
                this.user = await getUserProfile();
            } catch (error) {
                console.error("Failed to fetch user profile:", error);
                throw error;
            }
        },
        async login(username: string, password: string) {
            try {
                const data = await login(username, password);
                this.accessToken = data.access;
                this.refreshToken = data.refresh;
                this.isAuthenticated = true;
                this.user = await getUserProfile();
                router.push("/");
            } catch (error) {
                console.error("Login failed:", error);
                throw error;
            }
        },
        async logout() {
            
            try {
                if (this.refreshToken) {
                    await logout();
                }   
                this.user = null;
                this.accessToken = null;
                this.refreshToken = null;
                this.isAuthenticated = false;
                localStorage.removeItem("accessToken");
                localStorage.removeItem("refresh_token");
                router.push("/");
            } catch (error) {
                console.error("Logout failed:", error);
                throw error;
            }
        },
        async refresh() {
            if (!this.refreshToken) return;
            try {
                const newAccessToken = await refreshToken();
                this.accessToken = newAccessToken;
                this.isAuthenticated = true;
            } catch (error) {
                console.error("Token refresh failed:", error);
                throw error;
            }
        },
    },
});
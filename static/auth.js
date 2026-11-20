// Токен хранится только до закрытия вкладки браузера.
async function apiFetch(url, options = {}) {
    const headers = new Headers(options.headers);
    const token = sessionStorage.getItem("library_token");
    if (token) {
        headers.set("Authorization", `Bearer ${token}`);
    }

    const response = await fetch(url, { ...options, headers });
    if (response.status === 401) {
        sessionStorage.removeItem("library_token");
    }
    return response;
}

async function getApiError(response) {
    if (response.status === 401) {
        return "Нужно войти в аккаунт. Если вы уже входили, войдите ещё раз.";
    }
    try {
        const error = await response.json();
        if (Array.isArray(error.detail)) {
            return error.detail.map((item) => item.msg).join("; ");
        }
        if (typeof error.detail === "string") {
            return error.detail;
        }
    } catch (error) {
        // Не каждый ответ с ошибкой содержит JSON.
    }
    return "Не удалось выполнить запрос.";
}

async function getCurrentUser() {
    if (!sessionStorage.getItem("library_token")) {
        return null;
    }
    const response = await apiFetch("/api/auth/me");
    if (response.status === 401) {
        return null;
    }
    if (!response.ok) {
        throw new Error(await getApiError(response));
    }
    return response.json();
}

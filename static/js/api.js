// API Configuration
const API_BASE_URL = 'http://localhost:8000/api';

// Token management
function getToken() {
    return localStorage.getItem('access_token');
}

function setToken(token) {
    localStorage.setItem('access_token', token);
}

function setRefreshToken(token) {
    localStorage.setItem('refresh_token', token);
}

function removeTokens() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
}

// API Request Helper
async function apiRequest(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`;
    const token = getToken();
    
    const headers = {
        'Content-Type': 'application/json',
        ...options.headers
    };
    
    if (token && !options.skipAuth) {
        headers['Authorization'] = `Bearer ${token}`;
    }
    
    try {
        const response = await fetch(url, {
            ...options,
            headers
        });
        
        if (response.status === 401) {
            // Token expired, try to refresh
            const refreshed = await refreshToken();
            if (refreshed) {
                // Retry the request
                headers['Authorization'] = `Bearer ${getToken()}`;
                const retryResponse = await fetch(url, {
                    ...options,
                    headers
                });
                return handleResponse(retryResponse);
            } else {
                // Refresh failed, redirect to login
                window.location.href = 'login.html';
                return null;
            }
        }
        
        return handleResponse(response);
    } catch (error) {
        console.error('API Request Error:', error);
        throw error;
    }
}

async function handleResponse(response) {
    const contentType = response.headers.get('content-type');
    const isJson = contentType && contentType.includes('application/json');
    const data = isJson ? await response.json() : await response.text();
    
    if (!response.ok) {
        throw {
            status: response.status,
            message: data.message || data.detail || 'Error en la solicitud',
            data: data
        };
    }
    
    return data;
}

async function refreshToken() {
    const refresh = localStorage.getItem('refresh_token');
    if (!refresh) return false;
    
    try {
        const response = await fetch(`${API_BASE_URL}/auth/refresh/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ refresh })
        });
        
        if (response.ok) {
            const data = await response.json();
            setToken(data.access);
            return true;
        }
        return false;
    } catch (error) {
        return false;
    }
}

// Authentication
async function login(username, password) {
    const data = await apiRequest('/auth/login/', {
        method: 'POST',
        skipAuth: true,
        body: JSON.stringify({ username, password })
    });
    
    setToken(data.access);
    setRefreshToken(data.refresh);
    return data;
}

function logout() {
    removeTokens();
    window.location.href = 'login.html';
}

// Check if user is authenticated
function isAuthenticated() {
    return !!getToken();
}

// Protect pages
function requireAuth() {
    if (!isAuthenticated()) {
        window.location.href = 'login.html';
    }
}

// Format currency
function formatCurrency(amount) {
    return new Intl.NumberFormat('es-CO', {
        style: 'currency',
        currency: 'COP',
        minimumFractionDigits: 0
    }).format(amount);
}

// Format date
function formatDate(dateString) {
    return new Date(dateString).toLocaleDateString('es-CO', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

// Show alert
function showAlert(message, type = 'success') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show position-fixed top-0 start-50 translate-middle-x mt-3`;
    alertDiv.style.zIndex = '9999';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    document.body.appendChild(alertDiv);
    
    setTimeout(() => {
        alertDiv.remove();
    }, 3000);
}

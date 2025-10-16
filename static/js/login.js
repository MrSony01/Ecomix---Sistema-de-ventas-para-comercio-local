// Login Form Handler
document.getElementById('loginForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const errorMessage = document.getElementById('errorMessage');
    
    errorMessage.classList.add('d-none');
    
    try {
        await login(username, password);
        window.location.href = 'index.html';
    } catch (error) {
        errorMessage.textContent = error.message || 'Credenciales inválidas';
        errorMessage.classList.remove('d-none');
    }
});

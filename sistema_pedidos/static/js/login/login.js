// document.addEventListener('DOMContentLoaded', () => {
//     document.getElementById('loginForm').addEventListener('submit', async (e) => {
//         e.preventDefault();

//         const username = document.getElementById('username').value;
//         const password = document.getElementById('password').value;

//         const response = await fetch('https://sebakaze.pythonanywhere.com/api/login/', {
//             method: 'POST',
//             headers: {
//                 'Content-Type': 'application/json',
//             },
//             body: JSON.stringify({ username, password }),
//         });

//         const result = await response.json();

//         const messageDiv = document.getElementById('message');

//         if (result.mensaje) {
//             messageDiv.textContent = result.mensaje;
//             setTimeout(() => {
//                 window.location.href = 'https://sebakaze.pythonanywhere.com/index'; // Redirigir a la página de pedidos
//             }, 2000);
//         } else {
//             messageDiv.textContent = result.error;
//         }
//     });
// });

document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('loginForm').addEventListener('submit', async (e) => {
        e.preventDefault();

        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;

        const response = await fetch('/login/', {  // Este es el formulario POST a la vista de Django
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',  // Formato tradicional para POST
            },
            body: `username=${username}&password=${password}&csrfmiddlewaretoken=${getCookie('csrftoken')}`
        });

        if (response.ok) {
            window.location.href = '/index/';  // Redirigir a la página de pedidos
        } else {
            alert('Error al iniciar sesión. Verifique sus credenciales.');
        }
    });
});

// Función para obtener el CSRF token
function getCookie(name) {
    const cookieValue = document.cookie.match('(^|;) ?' + name + '=([^;]*)(;|$)');
    return cookieValue ? cookieValue[2] : null;
}


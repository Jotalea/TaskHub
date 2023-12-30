document.addEventListener("DOMContentLoaded", function () {
    // Simula el tiempo de carga
    setTimeout(function () {
        const loaderContainer = document.querySelector(".loader-container");
        loaderContainer.classList.add("hidden");
        document.body.style.overflow = 'auto';
    }, 2000); // Tiempo de carga simulado: 2 segundos
});

// Assume this is the function executed on page load
function cargarPagina() {
    // Check if there is a username saved in the cookie
    const nombreUsuario = obtenerNombreUsuario();
    if (nombreUsuario) {
        // Autofill the form
        document.getElementById('username').value = nombreUsuario;
    }
}

// Function to save the username in the cookie
function guardarNombreUsuario(nombreUsuario) {
    document.cookie = `nombreUsuario=${nombreUsuario}; expires=Thu, 31 Dec 2030 23:59:59 UTC; path=/`;
}

// Function to get the username from the cookie
function obtenerNombreUsuario() {
    const cookies = document.cookie.split("; ");
    for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].split("=");
        if (cookie[0] === "nombreUsuario") {
            return cookie[1];
        }
    }
    return null;
}

function compartir(taskID, materia) {
    const pageUrl = 'https://taskhub.jotaleaex.repl.co/tarea/' + taskID;
    const title = 'Tarea de ' + materia;
    const textToCopy = 'Respuestas de la tarea de ' + materia + ' en TaskHub';

    if (navigator.share) {
        navigator.share({
            title: title, // document.title
            text: textToCopy,
            url: pageUrl
    })
        .then(() => console.log('Este pibe se sabe la de compartir'))
        .catch((error) => console.error('Error al compartir:', error));
    } else {
        const textToCopy = 'Respuestas de la tarea de ' + materia + ' en TaskHub\n' + pageUrl;
        copyTextToClipboard(textToCopy);
        showNotification('Enlace copiado en el portapapeles');
    }
}

function copyTextToClipboard(text) {
  navigator.clipboard.writeText(text)
    .then(() => console.log("Text copied: " + text))
    .catch((err) => console.error('Error copying to clipboard: ', err));
}

function copyElementToClipboard() {
  var copyText = document.getElementById("myInput");
  navigator.clipboard.writeText(copyText.value)
    .then(() => alert("Texto copiado: " + copyText.value))
    .catch((err) => console.error('Error al copiar al portapapeles: ', err));
}

function copyURLToClipboard() {
    var dummyElement = document.createElement("textarea");
    document.body.appendChild(dummyElement);
    dummyElement.value = window.location.href;
    dummyElement.select();
    document.execCommand("copy");
    document.body.removeChild(dummyElement);
    alert("Link copied to clipboard!");
}

function showNotification(message) {
  const notification = document.createElement('div');
  notification.className = 'notification';
  notification.innerHTML = `
    <span class="noselect">${message}</span>
    <span class="close-btn noselect" onclick="closeNotification(this.parentNode)">⨯</span>
  `;

  document.body.appendChild(notification);

  setTimeout(() => {
    notification.style.top = '20px'; // Cuanto baja la notificación
  }, 10);

  // Cerrar la notificación después de 5 segundos
  setTimeout(() => {
    closeNotification(notification);
  }, 5000);
}

function closeNotification(notification) {
  notification.style.top = '-100px';
  setTimeout(() => {
    notification.remove();
  }, 5000);
}

// Aceptar "galletitas" y llevarse el banner
function aceptarCookies() {
    document.getElementById('cookie-banner').style.display = 'none';
    // Guardar una galletita que diga que el pibe ya aceptó las galletitas
    document.cookie = "cookiesAceptadas=true; expires=Thu, 31 Dec 2030 23:59:59 UTC; path=/";
}

// Ver si el usuario aceptó las "galletitas"
function verificarCookiesAceptadas() {
    const cookies = document.cookie.split("; ");
    for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].split("=");
        if (cookie[0] === "cookiesAceptadas" && cookie[1] === "true") {
            // Ya aceptó las cookies, sacar el banner
            document.getElementById('cookie-banner').style.display = 'none';
            break;
        }
    }
}

// document.getElementById('mostrarBtn').addEventListener('click', mostrarVentana);

function mostrarVentana() {
    document.getElementById('ventanaEmergente').classList.remove('oculto');
}

function cerrarVentana() {
    document.getElementById('ventanaEmergente').classList.add('oculto');
}

// Check cookies on page load
verificarCookiesAceptadas();
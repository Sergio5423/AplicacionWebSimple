document.getElementById('btnEnviar').addEventListener('click', function () {
    const nombre = document.getElementsByName('nombre')[0].value;
    const apellido = document.getElementsByName('apellido')[0].value;
    const telefono = document.getElementsByName('telefono')[0].value;
    const correo = document.getElementsByName('correo')[0].value;

    fetch('http://127.0.0.1:8000/contactos/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ nombre, apellido, telefono, correo })
    })
    .then(response => response.json())
    .then(data => alert('Éxito: ' + data.message))
    .catch(error => console.error('Error:', error));
});

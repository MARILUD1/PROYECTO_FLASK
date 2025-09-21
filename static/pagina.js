document.addEventListener('DOMContentLoaded', function() {
    const passwordInput = document.getElementById('password');
    const toggleButton = document.getElementById('togglePassword');
    const eyeIcon = document.getElementById('eyeIcon');
    let timeoutId;

    if (toggleButton) {
        toggleButton.addEventListener('mousedown', function(event) {
            event.preventDefault(); // Previene que el campo de entrada pierda el foco
            passwordInput.type = 'text';
            eyeIcon.classList.remove('bi-eye-slash');
            eyeIcon.classList.add('bi-eye');

            // Oculta la contraseña después de 1 segundo
            timeoutId = setTimeout(() => {
                passwordInput.type = 'password';
                eyeIcon.classList.remove('bi-eye');
                eyeIcon.classList.add('bi-eye-slash');
            }, 1000);
        });

        toggleButton.addEventListener('mouseup', function() {
            clearTimeout(timeoutId);
            passwordInput.type = 'password';
            eyeIcon.classList.remove('bi-eye');
            eyeIcon.classList.add('bi-eye-slash');
        });

        // Evitar que el ojo se quede en "visible" si se suelta el mouse fuera del botón
        toggleButton.addEventListener('mouseleave', function() {
            clearTimeout(timeoutId);
            passwordInput.type = 'password';
            eyeIcon.classList.remove('bi-eye');
            eyeIcon.classList.add('bi-eye-slash');
        });
    }
});
// La siguiente línea asegura que el código se ejecute una vez que la página esté completamente cargada.
document.addEventListener("DOMContentLoaded", () => {
    // --- Lógica para el botón "Cambiar contenido" ---
    const boton = document.getElementById("boton");
    const descripcion = document.getElementById("descripcion");

    if (boton && descripcion) {
        boton.addEventListener("click", () => {
            descripcion.innerHTML = `
                <strong>En cambio:</strong><br>
                <strong>¿Qué es JavaScript?</strong><br>
                <em>JavaScript es esencialmente el cerebro de la mayoría de los sitios web modernos. 
                Es lo que hace que las páginas sean interactivas, dinámicas y ofrezcan una experiencia de usuario fluida y receptiva. 
                Sin JavaScript, la web sería mucho más estática y menos atractiva.</em>
            `;
        });
    }

    // --- Lógica para la Galería de imágenes (si la necesitas) ---
    const inputUrl = document.getElementById("imageUrl");
    const addBtn = document.getElementById("addImageBtn");
    const deleteBtn = document.getElementById("deleteImageBtn");
    const gallery = document.getElementById("gallery");

    let selectedImage = null; 

    if (inputUrl && addBtn && deleteBtn && gallery) {
        function deselectAllImages() {
            document.querySelectorAll(".gallery-image").forEach((el) => {
                el.classList.remove("selected");
            });
        }

        addBtn.addEventListener("click", () => {
            const url = inputUrl.value.trim();
            if (url === "") {
                alert("Por favor, ingresa una URL válida para la imagen.");
                return;
            }

            const img = document.createElement("img");
            img.src = url;
            img.classList.add("gallery-image");

            img.addEventListener("click", () => {
                deselectAllImages(); 
                img.classList.add("selected");
                selectedImage = img; 
            });

            gallery.appendChild(img);
            inputUrl.value = "";
            selectedImage = null; 
        });

        deleteBtn.addEventListener("click", () => {
            if (selectedImage) {
                if (confirm("¿Estás seguro de que quieres eliminar la imagen seleccionada?")) {
                    selectedImage.remove();
                    selectedImage = null;
                }
            } else {
                alert("Por favor, selecciona una imagen para eliminar.");
            }
        });

        inputUrl.addEventListener("keydown", (event) => {
            if (event.key === "Enter") {
                event.preventDefault();
                addBtn.click();
            }
        });
    } else {
        console.error("Uno o más elementos de la galería no fueron encontrados en el DOM.");
    }

    // --- Lógica para la Lista de Tareas (si la necesitas) ---
    const taskInput = document.getElementById("taskInput");
    const addTaskBtn = document.getElementById("addTaskBtn");
    const taskList = document.getElementById("taskList");
    const botonRosa = document.getElementById("cambiarColorRosaBtn");

    if (botonRosa) {
        botonRosa.addEventListener("click", () => {
            document.body.style.backgroundColor = "pink";
        });
    }

    if (taskInput && addTaskBtn && taskList) {
        addTaskBtn.addEventListener("click", () => {
            const taskText = taskInput.value.trim();
            if (taskText !== "") {
                const listItem = document.createElement("li");
                listItem.classList.add("list-group-item");
                listItem.textContent = taskText;

                const deleteSpan = document.createElement("span");
                deleteSpan.textContent = " X";
                deleteSpan.style.cursor = "pointer";
                deleteSpan.style.float = "right";
                deleteSpan.style.color = "red";
                deleteSpan.addEventListener("click", () => {
                    listItem.remove();
                });
                listItem.appendChild(deleteSpan);

                taskList.appendChild(listItem);
                taskInput.value = "";
            } else {
                alert("Por favor, escribe una inquietud.");
            }
        });

        taskInput.addEventListener("keydown", (event) => {
            if (event.key === "Enter") {
                event.preventDefault();
                addTaskBtn.click();
            }
        });
    }
});
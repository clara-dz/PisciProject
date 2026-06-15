const searchForm = document.getElementById("search-form");
const searchInput = document.getElementById("search-input");
const resultsContainer = document.getElementById("components-results");
const message = document.getElementById("search-message");

function getSelectedType() {
    const selectedType = document.querySelector('input[name="tipo"]:checked');

    if (!selectedType) {
        return "";
    }

    return selectedType.value;
}

async function searchComponents(event) {
    event.preventDefault();

    const searchTerm = searchInput.value.trim();
    const selectedType = getSelectedType();

    const params = new URLSearchParams();

    if (searchTerm) {
        params.append("q", searchTerm);
    }

    if (selectedType) {
        params.append("type", selectedType);
    }

    const url = `/catalog/components?${params.toString()}`;

    message.textContent = "Buscando componentes...";
    resultsContainer.innerHTML = "";

    try {
        const response = await fetch(url);
        const result = await response.json();

        if (!response.ok || result.status !== "sucesso") {
            message.textContent = result.message || "Erro ao buscar componentes.";
            return;
        }

        renderComponents(result.data);

    } catch (error) {
        console.error(error);
        message.textContent = "Erro ao conectar com o servidor.";
    }
}

function renderComponents(components) {
    resultsContainer.innerHTML = "";

    if (!components || components.length === 0) {
        message.textContent = "Nenhum componente encontrado.";
        return;
    }

    message.textContent = `${components.length} componente(s) encontrado(s).`;

    components.forEach(component => {
        const card = document.createElement("article");
        card.classList.add("component-card");

        const imageHtml = component.Image
            ? `<img src="${component.Image}" alt="${component.Name}" class="component-image">`
            : `<div class="component-image-placeholder">Sem imagem</div>`;

        card.innerHTML = `
            ${imageHtml}

            <div class="component-info">
                <h3>${component.Name}</h3>
                <p><strong>Fabricante:</strong> ${component.Manufacturer || "Não informado"}</p>
                <p><strong>Categoria:</strong> ${component.Categoria}</p>
                <p><strong>ID:</strong> ${component.ID}</p>

                <button 
                    type="button" 
                    class="add-component-button"
                    data-id="${component.ID}"
                    data-category="${component.Categoria}"
                >
                    Adicionar ao projeto
                </button>
            </div>
        `;

        resultsContainer.appendChild(card);
    });
}

searchForm.addEventListener("submit", searchComponents);

document.querySelectorAll('input[name="tipo"]').forEach(radio => {
    radio.addEventListener("change", async () => {
        const fakeEvent = {
            preventDefault: () => {}
        };

        await searchComponents(fakeEvent);
    });
});

window.addEventListener("load", async () => {
    const fakeEvent = {
        preventDefault: () => {}
    };

    await searchComponents(fakeEvent);
});
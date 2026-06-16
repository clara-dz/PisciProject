const searchForm = document.getElementById("search-form");
const searchInput = document.getElementById("search-input");
const resultsContainer = document.getElementById("components-results");
const message = document.getElementById("search-message");

function normalizeType(type) {
    const map = {
        CPU: "CPU",
        GPU: "GPU",
        RAM: "RAM",
        MEM_RAM: "RAM",
        MOTHERBOARD: "MOTHERBOARD",
        MotherBoard: "MOTHERBOARD",
        PLACA_MAE: "MOTHERBOARD",
        SSD: "SSD",
        POWER: "POWER",
        Power: "POWER",
        FONTE: "POWER"
    };

    return map[type] || type || "";
}

function getTypeFromUrl() {
    const params = new URLSearchParams(window.location.search);
    return normalizeType(params.get("tipo") || params.get("type") || "");
}

function selectTypeFromUrl() {
    const typeFromUrl = getTypeFromUrl();
    if (!typeFromUrl) return;

    const radio = document.querySelector(`input[name="tipo"][value="${typeFromUrl}"]`);
    if (radio) radio.checked = true;
}

function getSelectedType() {
    const selectedType = document.querySelector('input[name="tipo"]:checked');
    return selectedType ? selectedType.value : "";
}

async function requestJson(url, options = {}) {
    const response = await fetch(url, {
        credentials: "same-origin",
        headers: {
            "Content-Type": "application/json",
            ...(options.headers || {})
        },
        ...options
    });

    let data = {};
    try {
        data = await response.json();
    } catch (error) {
        data = {};
    }

    if (!response.ok || data.status === "erro") {
        throw new Error(data.message || "Erro ao conectar com o servidor.");
    }

    return data;
}

async function searchComponents(event) {
    if (event) event.preventDefault();

    const searchTerm = searchInput.value.trim();
    const selectedType = getSelectedType();
    const params = new URLSearchParams();

    if (searchTerm) params.append("q", searchTerm);
    if (selectedType) params.append("type", selectedType);

    const url = `/catalog/components?${params.toString()}`;

    message.textContent = "Buscando componentes...";
    resultsContainer.innerHTML = "";

    try {
        const result = await requestJson(url, { method: "GET" });
        renderComponents(result.data || []);
    } catch (error) {
        console.error(error);
        message.textContent = error.message;
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

async function addComponentToProject(componentId, category) {
    message.textContent = "Adicionando componente ao projeto...";

    try {
        await requestJson("/project/add-component", {
            method: "POST",
            body: JSON.stringify({
                component_id: componentId,
                tipo: category
            })
        });

        window.location.href = "montarprojeto.html";
    } catch (error) {
        console.error(error);
        message.textContent = error.message;
    }
}

searchForm.addEventListener("submit", searchComponents);

resultsContainer.addEventListener("click", event => {
    const button = event.target.closest(".add-component-button");
    if (!button) return;

    addComponentToProject(button.dataset.id, button.dataset.category);
});

document.querySelectorAll('input[name="tipo"]').forEach(radio => {
    radio.addEventListener("change", searchComponents);
});

window.addEventListener("load", async () => {
    selectTypeFromUrl();
    await searchComponents();
});

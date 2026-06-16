const projectMessage = document.getElementById("project-message");
const compatibilityResult = document.getElementById("compatibility-result");
const saveProjectForm = document.getElementById("save-project-form");
const projectNameInput = document.getElementById("project-name");
const projectDescriptionInput = document.getElementById("project-description");
const clearProjectButton = document.getElementById("clear-project-button");
const checkCompatibilityButton = document.getElementById("check-compatibility-button");

const SLOT_LABELS = {
    CPU: "CPU",
    MotherBoard: "Placa-mãe",
    GPU: "GPU",
    MEM_RAM: "RAM",
    SSD: "HD/SSD",
    Power: "Fonte"
};

function setProjectMessage(text, isError = false) {
    if (!projectMessage) return;
    projectMessage.textContent = text || "";
    projectMessage.style.color = isError ? "red" : "green";
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
        const message = data.message || "Erro ao conectar com o servidor.";
        throw new Error(message);
    }

    return data;
}

function getComponentName(component) {
    if (!component) return "Nenhum componente selecionado";
    return component.Name || component.name || `Componente #${component.ID || component.id}`;
}

function getComponentId(component) {
    if (!component) return null;
    return component.ID || component.CPU_ID || component.MB_ID || component.GPU_ID || component.MEM_RAM_ID || component.SSD_ID || component.POWER_ID || component.id;
}

function renderSlots(detalhes = {}) {
    Object.keys(SLOT_LABELS).forEach(slot => {
        const span = document.getElementById(`slot-${slot}`);
        if (!span) return;

        const component = detalhes[slot];
        const componentName = getComponentName(component);
        const componentId = getComponentId(component);

        span.textContent = componentId ? `${componentName} (ID: ${componentId})` : componentName;
    });
}

function renderCompatibility(compatibilidade) {
    if (!compatibilityResult) return;

    if (!compatibilidade) {
        compatibilityResult.innerHTML = "<p>Compatibilidade ainda não verificada.</p>";
        return;
    }

    const warnings = compatibilidade.warnings || [];
    const isCompatible = Boolean(compatibilidade.is_compatible);

    if (isCompatible && warnings.length === 0) {
        compatibilityResult.innerHTML = `<p class="compatibility-ok">Projeto compatível até agora.</p>`;
        return;
    }

    const title = isCompatible
        ? "Projeto funciona, mas possui avisos:"
        : "Projeto incompatível:";

    const items = warnings.length
        ? warnings.map(warning => `<li>${warning}</li>`).join("")
        : "<li>Existe uma incompatibilidade, mas o backend não retornou detalhes.</li>";

    compatibilityResult.innerHTML = `
        <div class="${isCompatible ? "compatibility-warning" : "compatibility-error"}">
            <p><strong>${title}</strong></p>
            <ul>${items}</ul>
        </div>
    `;
}

function fillProjectForm(data) {
    if (projectNameInput && data.project_name) {
        projectNameInput.value = data.project_name === "Rascunho Novo" ? "" : data.project_name;
    }

    if (projectDescriptionInput && data.project_description) {
        projectDescriptionInput.value = data.project_description;
    }
}

function renderProject(data) {
    renderSlots(data.detalhes || {});
    renderCompatibility(data.compatibilidade);
    fillProjectForm(data);
}

async function loadCurrentProject() {
    try {
        const data = await requestJson("/project/current");
        renderProject(data);
    } catch (error) {
        setProjectMessage(error.message, true);
    }
}

async function removeComponent(slot) {
    try {
        const data = await requestJson("/project/remove-component", {
            method: "POST",
            body: JSON.stringify({ tipo: slot })
        });

        renderProject(data);
        setProjectMessage(data.message || "Componente removido.");
    } catch (error) {
        setProjectMessage(error.message, true);
    }
}

async function clearProject() {
    try {
        const data = await requestJson("/project/start", {
            method: "POST",
            body: JSON.stringify({})
        });

        renderProject(data);

        if (projectNameInput) projectNameInput.value = "";
        if (projectDescriptionInput) projectDescriptionInput.value = "";

        setProjectMessage(data.message || "Projeto limpo.");
    } catch (error) {
        setProjectMessage(error.message, true);
    }
}

async function saveProject(event) {
    event.preventDefault();

    const name = projectNameInput.value.trim();
    const description = projectDescriptionInput.value.trim();

    try {
        const data = await requestJson("/project/save", {
            method: "POST",
            body: JSON.stringify({ name, description })
        });

        setProjectMessage(data.message || "Projeto salvo com sucesso.");
        await loadCurrentProject();
    } catch (error) {
        setProjectMessage(error.message, true);
    }
}

function setupEvents() {
    document.querySelectorAll(".remove-slot-button").forEach(button => {
        button.addEventListener("click", () => {
            const slot = button.dataset.slot;
            if (slot) removeComponent(slot);
        });
    });

    if (clearProjectButton) {
        clearProjectButton.addEventListener("click", clearProject);
    }

    if (checkCompatibilityButton) {
        checkCompatibilityButton.addEventListener("click", loadCurrentProject);
    }

    if (saveProjectForm) {
        saveProjectForm.addEventListener("submit", saveProject);
    }
}

window.addEventListener("load", async () => {
    setupEvents();
    await loadCurrentProject();
});

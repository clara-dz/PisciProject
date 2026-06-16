const projectMessage = document.getElementById("project-message");
const saveProjectMessage = document.getElementById("save-project-message");
const compatibilityResult = document.getElementById("compatibility-result");
const saveProjectForm = document.getElementById("save-project-form");
const projectNameInput = document.getElementById("project-name");
const projectDescriptionInput = document.getElementById("project-description");
const clearProjectButton = document.getElementById("clear-project-button");
const checkCompatibilityButton = document.getElementById("check-compatibility-button");

let isSavingProject = false;

let projectWasSaved = false;
let isNavigatingToSearch = false;
let isClearingProject = false;

const SLOT_LABELS = {
    CPU: "CPU",
    MotherBoard: "Placa-mãe",
    GPU: "GPU",
    MEM_RAM: "RAM",
    SSD: "HD/SSD",
    Power: "Fonte"
};

const SLOT_TO_CATEGORY = {
    CPU: "CPU",
    MotherBoard: "MOTHERBOARD",
    GPU: "GPU",
    MEM_RAM: "RAM",
    SSD: "SSD",
    Power: "POWER"
};

const SLOT_ALIASES = {
    CPU: ["CPU", "Cpu", "cpu"],
    MotherBoard: ["MotherBoard", "MOTHERBOARD", "motherboard", "MB", "Mb", "mb"],
    GPU: ["GPU", "Gpu", "gpu"],
    MEM_RAM: ["MEM_RAM", "RAM", "Ram", "ram", "mem_ram"],
    SSD: ["SSD", "Ssd", "ssd"],
    Power: ["Power", "POWER", "Fonte", "FONTE", "power", "fonte"]
};

const ID_FIELDS_BY_SLOT = {
    CPU: ["ID", "id", "CPU_ID", "cpu_id"],
    MotherBoard: ["ID", "id", "MB_ID", "mb_id", "MotherBoard_ID", "motherboard_id"],
    GPU: ["ID", "id", "GPU_ID", "gpu_id"],
    MEM_RAM: ["ID", "id", "MEM_RAM_ID", "mem_ram_id", "RAM_ID", "ram_id"],
    SSD: ["ID", "id", "SSD_ID", "ssd_id"],
    Power: ["ID", "id", "POWER_ID", "power_id", "Fonte_ID", "fonte_id"]
};

const HIDDEN_FIELDS = new Set([
    "Image",
    "Image_URL",
    "Image_Url",
    "image",
    "image_url",
    "Image_Data",
    "Name",
    "name",
    "Product_Name",
    "Model",
    "model"
]);

function setProjectMessage(text, isError = false) {
    if (!projectMessage) return;

    projectMessage.textContent = text || "";
    projectMessage.style.color = isError ? "red" : "green";
}

function setSaveProjectMessage(text, isError = false) {
    if (!saveProjectMessage) return;

    saveProjectMessage.textContent = text || "";
    saveProjectMessage.style.color = isError ? "red" : "green";
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

function getValueByKeys(object, keys) {
    if (!object) return null;

    for (const key of keys) {
        if (object[key] !== undefined && object[key] !== null && object[key] !== "") {
            return object[key];
        }
    }

    return null;
}

function getSlotValue(object, slot) {
    if (!object) return null;

    const aliases = SLOT_ALIASES[slot] || [slot];

    for (const alias of aliases) {
        if (object[alias] !== undefined && object[alias] !== null) {
            return object[alias];
        }
    }

    return null;
}

function getComponentName(component, slot) {
    if (!component) {
        return "Nenhum componente selecionado";
    }

    return (
        component.Name ||
        component.name ||
        component.Product_Name ||
        component.Model ||
        component.model ||
        component.CPU_Name ||
        component.GPU_Name ||
        component.MB_Name ||
        component.RAM_Name ||
        component.SSD_Name ||
        component.Power_Name ||
        component.Component_Name ||
        component.component_name ||
        `${SLOT_LABELS[slot]} selecionado`
    );
}

function getComponentId(component, slot) {
    if (!component) return null;

    const specificId = getValueByKeys(component, ID_FIELDS_BY_SLOT[slot] || []);
    if (specificId !== null) return specificId;

    for (const [key, value] of Object.entries(component)) {
        const normalizedKey = key.toLowerCase();

        if (
            normalizedKey === "id" ||
            normalizedKey.endsWith("_id") ||
            normalizedKey.endsWith("id")
        ) {
            if (value !== undefined && value !== null && value !== "") {
                return value;
            }
        }
    }

    return null;
}

function getComponentImage(component) {
    if (!component) return null;

    return (
        component.Image ||
        component.image ||
        component.Image_URL ||
        component.Image_Url ||
        component.image_url ||
        component.Photo ||
        component.photo ||
        component.Picture ||
        component.picture ||
        null
    );
}

function formatFieldName(key) {
    const labels = {
        ID: "ID",
        id: "ID",

        CPU_ID: "ID",
        cpu_id: "ID",
        MB_ID: "ID",
        mb_id: "ID",
        GPU_ID: "ID",
        gpu_id: "ID",
        MEM_RAM_ID: "ID",
        mem_ram_id: "ID",
        SSD_ID: "ID",
        ssd_id: "ID",
        POWER_ID: "ID",
        power_id: "ID",

        Manufacturer: "Fabricante",
        manufacturer: "Fabricante",
        Categoria: "Categoria",
        category: "Categoria",

        CPU_Socket: "Soquete",
        CPU_TDP: "TDP",
        Have_GPU: "Vídeo integrado",

        MB_Socket: "Soquete",
        Chipset: "Chipset",
        form_factor: "Formato",
        dimensions_mm: "Dimensões",
        Slots_Ram: "Slots de RAM",
        Ram_type: "Tipo de RAM",
        Ram_max_cap: "Capacidade máxima de RAM",
        Ram_max_vel: "Velocidade máxima de RAM",
        Pcie_Version: "Versão PCIe",
        Pcie_x16_slots: "Slots PCIe x16",
        m2_slots: "Slots M.2",
        M2_pcie_version: "PCIe do M.2",
        Sata_ports: "Portas SATA",

        Tgp: "TGP",
        Pcie_8pin_Count: "PCIe 8 pinos",
        Pcie_6pin_Count: "PCIe 6 pinos",
        Pcie_12vhpwr_Count: "12VHPWR",

        RAM_type: "Tipo de RAM",
        Velocity: "Velocidade",
        Capacity: "Capacidade",
        Cas_Latency: "Latência CAS",

        Format: "Formato",
        Interface: "Interface",

        Pot_Watts: "Potência",
        Efficiency: "Eficiência",
        Modular: "Modular",
        Cpu_8pin_Count: "CPU 8 pinos",
        sata_power_count: "Conectores SATA"
    };

    return labels[key] || key.replaceAll("_", " ");
}

function formatFieldValue(value) {
    if (value === null || value === undefined || value === "") {
        return "Não informado";
    }

    if (typeof value === "boolean") {
        return value ? "Sim" : "Não";
    }

    if (value === 0 || value === 1) {
        return value;
    }

    return value;
}

function shouldShowField(key, value) {
    if (HIDDEN_FIELDS.has(key)) return false;
    if (value === null || value === undefined || value === "") return false;

    return true;
}

function renderSpecs(component, slot) {
    const componentId = getComponentId(component, slot);
    const category = component.Categoria || component.category || SLOT_TO_CATEGORY[slot] || SLOT_LABELS[slot];

    const manufacturer = component.Manufacturer || component.manufacturer || "Não informado";

    const fixedFields = `
        <p><strong>Fabricante:</strong> ${formatFieldValue(manufacturer)}</p>
        <p><strong>Categoria:</strong> ${formatFieldValue(category)}</p>
        <p><strong>ID:</strong> ${formatFieldValue(componentId)}</p>
    `;

    const ignoredFields = new Set([
        "ID",
        "id",
        "CPU_ID",
        "cpu_id",
        "MB_ID",
        "mb_id",
        "GPU_ID",
        "gpu_id",
        "MEM_RAM_ID",
        "mem_ram_id",
        "SSD_ID",
        "ssd_id",
        "POWER_ID",
        "power_id",
        "Manufacturer",
        "manufacturer",
        "Categoria",
        "category"
    ]);

    const dynamicFields = Object.entries(component)
        .filter(([key, value]) => shouldShowField(key, value))
        .filter(([key]) => !ignoredFields.has(key))
        .map(([key, value]) => {
            return `<p><strong>${formatFieldName(key)}:</strong> ${formatFieldValue(value)}</p>`;
        })
        .join("");

    return fixedFields + dynamicFields;
}

function renderEmptySlot(slot) {
    return `
        <div class="empty-selected-component">
            <h4>${SLOT_LABELS[slot]}</h4>
            <p>Nenhum componente selecionado</p>
        </div>

        <button type="button" class="remove-slot-button" data-slot="${slot}">
            Remover
        </button>
    `;
}

function renderFallbackSelectedSlot(slot, selectedId) {
    return `
        <div class="empty-selected-component selected-without-details">
            <h4>${SLOT_LABELS[slot]}</h4>
            <p>Componente selecionado.</p>
            <p><strong>ID:</strong> ${selectedId}</p>
            <small>Os detalhes desse componente não foram retornados pelo backend.</small>
        </div>

        <button type="button" class="remove-slot-button" data-slot="${slot}">
            Remover
        </button>
    `;
}

function renderSelectedComponentCard(component, slot) {
    const componentName = getComponentName(component, slot);
    const componentImage = getComponentImage(component);

    const imageHtml = componentImage
        ? `<img src="${componentImage}" alt="${componentName}" class="component-image">`
        : "";

    return `
        <article class="component-card selected-component-card">
            ${imageHtml}

            <div class="component-info">
                <h3>${componentName}</h3>
                ${renderSpecs(component, slot)}

                <button 
                    type="button" 
                    class="remove-slot-button"
                    data-slot="${slot}"
                >
                    Remover
                </button>
            </div>
        </article>
    `;
}

function renderSlots(detalhes = {}, projeto = {}) {
    Object.keys(SLOT_LABELS).forEach(slot => {
        const card = document.querySelector(`.project-slot-card[data-slot="${slot}"]`);
        if (!card) return;

        const component = getSlotValue(detalhes, slot);
        const selectedId = getSlotValue(projeto, slot);
        const componentId = getComponentId(component, slot);

        if (component) {
            card.classList.add("has-component");
            card.innerHTML = renderSelectedComponentCard(component, slot);
        } else if (selectedId) {
            card.classList.add("has-component");
            card.innerHTML = renderFallbackSelectedSlot(slot, selectedId);
        } else {
            card.classList.remove("has-component");
            card.innerHTML = renderEmptySlot(slot);
        }
    });

    setupRemoveButtons();
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
        compatibilityResult.innerHTML = `
            <p class="compatibility-ok">Projeto compatível até agora.</p>
        `;
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
    if (projectNameInput && data.project_name !== undefined && data.project_name !== null) {
        projectNameInput.value = data.project_name === "Rascunho Novo"
            ? ""
            : data.project_name;
    }

    if (projectDescriptionInput && data.project_description !== undefined && data.project_description !== null) {
        projectDescriptionInput.value = data.project_description;
    }
}

function renderProject(data) {
    console.log("Projeto atual retornado pelo backend:", data);

    renderSlots(data.detalhes || {}, data.projeto || {});
    renderCompatibility(data.compatibilidade);
    fillProjectForm(data);
}

async function loadCurrentProject() {
    try {
        const data = await requestJson("/project/current");
        renderProject(data);
        return data;
    } catch (error) {
        setProjectMessage(error.message, true);
        throw error;
    }
}

async function removeComponent(slot) {
    try {
        setSaveProjectMessage("");

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

    isClearingProject = true;

    try {
        setSaveProjectMessage("");

        const data = await requestJson("/project/start", {
            method: "POST",
            body: JSON.stringify({})
        });

        renderProject(data);

        if (projectNameInput) {
            projectNameInput.value = "";
        }

        if (projectDescriptionInput) {
            projectDescriptionInput.value = "";
        }

        setProjectMessage(data.message || "Projeto limpo.");
    } catch (error) {
        setProjectMessage(error.message, true);
    }
}

async function saveProject(event) {
    event.preventDefault();

    if (isSavingProject) {
        return;
    }

    isSavingProject = true;

    const saveButton = saveProjectForm
        ? saveProjectForm.querySelector("button[type='submit']")
        : null;

    const name = projectNameInput ? projectNameInput.value.trim() : "";
    const description = projectDescriptionInput ? projectDescriptionInput.value.trim() : "";

    setSaveProjectMessage("");

    if (saveButton) {
        saveButton.disabled = true;
        saveButton.textContent = "Salvando...";
    }

    try {
        const data = await requestJson("/project/save", {
            method: "POST",
            body: JSON.stringify({
                name: name,
                description: description
            })
        });

        projectWasSaved = true;

        await loadCurrentProject();

        setSaveProjectMessage(data.message || "Projeto salvo com sucesso.");
        setProjectMessage("");
    } catch (error) {
        setSaveProjectMessage(error.message, true);
    } finally {
        isSavingProject = false;

        if (saveButton) {
            saveButton.disabled = false;
            saveButton.textContent = "Salvar Projeto";
        }
    }
}

function setupRemoveButtons() {
    document.querySelectorAll(".remove-slot-button").forEach(button => {
        button.onclick = () => {
            const slot = button.dataset.slot;

            if (slot) {
                removeComponent(slot);
            }
        };
    });
}

function setupEvents() {
    setupRemoveButtons();

    document.querySelectorAll(".add-components-panel a").forEach(link => {
    link.addEventListener("click", () => {
        isNavigatingToSearch = true;
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

function discardUnsavedProjectOnExit() {
    if (projectWasSaved || isNavigatingToSearch || isClearingProject) {
        return;
    }

    const payload = JSON.stringify({});

    if (navigator.sendBeacon) {
        const blob = new Blob([payload], { type: "application/json" });
        navigator.sendBeacon("/project/discard", blob);
    } else {
        fetch("/project/discard", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: payload,
            keepalive: true
        });
    }
}

window.addEventListener("pagehide", discardUnsavedProjectOnExit);

window.addEventListener("load", async () => {
    setupEvents();

    try {
        await loadCurrentProject();
    } catch (error) {
        console.error("Erro ao carregar projeto atual:", error);
    }
});
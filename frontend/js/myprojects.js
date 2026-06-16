const myProjectsSection = document.getElementById("my-projects-section");
const myProjectsList = document.getElementById("my-projects-list");
const myProjectsMessage = document.getElementById("my-projects-message");

function setMyProjectsMessage(text, isError = false) {
    if (!myProjectsMessage) return;

    myProjectsMessage.textContent = text || "";
    myProjectsMessage.style.color = isError ? "red" : "green";
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

function renderProjectCard(project) {
    const compatibilityText = project.is_compatible
        ? "Compatível"
        : "Incompatível";

    const compatibilityClass = project.is_compatible
        ? "project-compatible"
        : "project-incompatible";

    return `
        <article class="saved-project-card">
            <h3>${project.name || "Projeto sem nome"}</h3>

            <p class="saved-project-description">
                ${project.description || "Sem descrição."}
            </p>

            <p class="${compatibilityClass}">
                ${compatibilityText}
            </p>

            <button
                type="button"
                class="load-project-button"
                data-project-id="${project.id}"
            >
                Modificar projeto
            </button>
        </article>
    `;
}

function setupLoadProjectButtons() {
    document.querySelectorAll(".load-project-button").forEach(button => {
        button.addEventListener("click", async () => {
            const projectId = button.dataset.projectId;

            if (!projectId) {
                setMyProjectsMessage("ID do projeto não encontrado.", true);
                return;
            }

            button.disabled = true;
            button.textContent = "Carregando...";

            try {
                await requestJson(`/project/load-project/${projectId}`);

                window.location.href = "montarprojeto.html";
            } catch (error) {
                setMyProjectsMessage(error.message, true);

                button.disabled = false;
                button.textContent = "Modificar projeto";
            }
        });
    });
}

async function loadMyProjects() {
    if (!myProjectsSection || !myProjectsList) return;

    try {
        const data = await requestJson("/project/my-projects");

        myProjectsSection.hidden = false;

        const projects = data.projetos || [];

        if (projects.length === 0) {
            myProjectsList.innerHTML = "";
            setMyProjectsMessage("Você ainda não possui projetos salvos.");
            return;
        }

        setMyProjectsMessage("");

        myProjectsList.innerHTML = projects
            .map(project => renderProjectCard(project))
            .join("");

        setupLoadProjectButtons();

    } catch (error) {
        /*
            Se o usuário não estiver logado, /project/my-projects deve retornar 401.
            Nesse caso, a seção "Meus projetos" fica escondida.
        */
        myProjectsSection.hidden = true;
    }
}

window.addEventListener("load", loadMyProjects);
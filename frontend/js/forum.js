const comentarioForm = document.getElementById("comentario-form");
const commentTopicInput = document.getElementById("comment-topic");
const commentContentInput = document.getElementById("comment-content");
const forumMessage = document.getElementById("forum-message");
const commentsList = document.getElementById("comments-list");

function setForumMessage(text, isError = false) {
    if (!forumMessage) return;

    forumMessage.textContent = text || "";
    forumMessage.style.color = isError ? "red" : "green";
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

function escapeHtml(value) {
    return String(value || "")
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}

function renderComment(comment) {
    const authorName = comment.AuthorName || comment.authorName || "Usuário";
    const content = comment.Content || comment.content || "";
    const topic = comment.ComponentType || comment.componentType || "Tópico";

    return `
        <article class="comentario">
            <h4>${escapeHtml(authorName)}</h4>
            <span class="comment-topic">${escapeHtml(topic)}</span>
            <p>${escapeHtml(content)}</p>
        </article>
    `;
}

async function loadComments() {
    if (!commentsList) return;

    try {
        const data = await requestJson("/forum/comments");
        const comments = data.data || [];

        if (comments.length === 0) {
            commentsList.innerHTML = `
                <p class="empty-comments-message">
                    Ainda não há comentários no fórum.
                </p>
            `;
            return;
        }

        commentsList.innerHTML = comments
            .map(comment => renderComment(comment))
            .join("");

    } catch (error) {
        commentsList.innerHTML = `
            <p class="empty-comments-message">
                Não foi possível carregar os comentários.
            </p>
        `;
    }
}

async function submitComment(event) {
    event.preventDefault();

    const content = commentContentInput.value.trim();
    const componentType = commentTopicInput.value;

    if (!content) {
        setForumMessage("O comentário não pode estar vazio.", true);
        return;
    }

    if (!componentType) {
        setForumMessage("Selecione uma categoria para o comentário.", true);
        return;
    }

    const submitButton = comentarioForm.querySelector("button[type='submit']");

    if (submitButton) {
        submitButton.disabled = true;
        submitButton.textContent = "Publicando...";
    }

    try {
        const data = await requestJson("/forum/comments", {
            method: "POST",
            body: JSON.stringify({
                content: content,
                componentType: componentType,
                componentId: null
            })
        });

        setForumMessage(data.message || "Comentário publicado com sucesso!");

        commentContentInput.value = "";
        commentTopicInput.value = "";

        await loadComments();

    } catch (error) {
        setForumMessage(error.message, true);
    } finally {
        if (submitButton) {
            submitButton.disabled = false;
            submitButton.textContent = "Publicar";
        }
    }
}

if (comentarioForm) {
    comentarioForm.addEventListener("submit", submitComment);
}

window.addEventListener("load", loadComments);
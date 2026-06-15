const form = document.getElementById("login-form");
const message = document.getElementById("login-message");

form.addEventListener("submit", async function (event) {
    event.preventDefault();

    const email = document.getElementById("email").value;
    const password = document.getElementById("senha").value;

    const dados = {
        email: email,
        password: password
    };

    try {
        const resposta = await fetch("/auth/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(dados)
        });

        const resultado = await resposta.json();

        if (!resposta.ok) {
            message.textContent = resultado.message;
            message.style.color = "red";
            return;
        }

        message.textContent = resultado.message;
        message.style.color = "green";

        window.location.href = "index.html";

    } catch (erro) {
        message.textContent = "Erro ao conectar com o servidor.";
        message.style.color = "red";
        console.error(erro);
    }
});
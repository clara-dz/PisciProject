const form = document.getElementById("register-form");
const message = document.getElementById("register-message");

form.addEventListener("submit", async function (event) {
    event.preventDefault();

    const name = document.getElementById("inputNome").value;
    const email = document.getElementById("inputEmail").value;
    const password = document.getElementById("inputSenha").value;
    const confirmPassword = document.getElementById("inputConfirmaSenha").value;

    const dados = {
        name: name,
        email: email,
        password: password,
        confirm_password: confirmPassword
    };

    try {
        const resposta = await fetch("/auth/register", {
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

        setTimeout(() => {
            window.location.href = "login.html";
        }, 1000);

    } catch (erro) {
        message.textContent = "Erro ao conectar com o servidor.";
        message.style.color = "red";
        console.error(erro);
    }
});
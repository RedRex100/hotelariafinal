async function enviar(event) {
    event.preventDefault();

    const nome = document.getElementById("nome").value.trim();
    const endereco = document.getElementById("endereco").value.trim();
    const cpf = document.getElementById("cpf").value.trim();
    const telefone = document.getElementById("telefone").value.trim();
    const email = document.getElementById("email").value.trim();
    const senha = document.getElementById("senha").value.trim();
    const confirmar = document.getElementById("confirmar-senha").value.trim();

    if (senha == confirmar) {
    const response = await fetch('/cadastro', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ nome, endereco, cpf, telefone, email, senha }),
    });

    const result = await response.json();
    const mensagem = document.getElementById("mensagem");

    if (response.ok) {
        window.location.href = result.redirect;
    } else {
        mensagem.textContent = "Erro ao cadastrar: " + result.message;
    }
}
else
{ 
    alert("As senhas não coincidem");
}
}

async function pagar(nomeUsuario, quarto) {
    const response = await fetch('/pagar', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ nomeUsuario, quarto})
    });

    const result = await response.json();
    const mensagem = document.getElementById("mensagem");

    if (response.ok) {
        mensagem.textContent = "Dívida quitada com sucesso!";
        window.location.reload();  // Recarrega a página para atualizar as reservas
    } else {
        mensagem.textContent = "Erro ao quitar a dívida: " + result.error;
    }
}

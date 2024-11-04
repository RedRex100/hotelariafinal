async function enviarConsumo() {
    // Coleta os valores dos itens de consumo
    const cerveja = parseInt(document.getElementById('cerveja').value) || 0;
    const suco = parseInt(document.getElementById('suco').value) || 0;
    const agua = parseInt(document.getElementById('agua').value) || 0;
    const lancheNatural = parseInt(document.getElementById('lanche-natural').value) || 0;
    const barrinhaCereal = parseInt(document.getElementById('barrinha-cereal').value) || 0;

    // Calcula o total de consumo
    let total = (cerveja*9) + (suco*8) + (agua*5) + (lancheNatural*10) + (barrinhaCereal*3.50);
    const dados =  {
        total: total
    };
    const response = await fetch('/frigobarar', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ dados }),
    });

    const result = await response.json();
    const mensagem = document.getElementById("mensagem");

    if (response.ok) {
        window.location.href = result.redirect;
    } else {
        mensagem.textContent = "Erro ao reservar: " + result.error;
    }
}

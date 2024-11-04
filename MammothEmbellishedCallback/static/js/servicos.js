async function enviarServicos(event) {
    event.preventDefault();

    const cafedamanhaSim = document.getElementById('cafe-da-manha-sim');
    const servicoDeQuartoSim = document.getElementById('servico-de-quarto-sim');
    const lavanderiaSim = document.getElementById('lavanderia-sim');
    const almocoSim = document.getElementById('almoco-sim');
    const jantaSim = document.getElementById('janta-sim');

    let custoServico = 0;

    // Cálculo do custo dos serviços selecionados
    if (servicoDeQuartoSim.checked) {
        custoServico += 150;
    }
    if (cafedamanhaSim.checked) {
        custoServico += 100;
    }
    if (lavanderiaSim.checked) {
        custoServico += 50;
    }
    if (almocoSim.checked) {
        custoServico += 100;
    }
    if (jantaSim.checked) {
        custoServico += 100;
    }

    const dados = {
        total: custoServico
    };

    const response = await fetch('/servicar', {
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

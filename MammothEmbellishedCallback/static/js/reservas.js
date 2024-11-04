function stringParaDate(dataString) {

    // Divide a string em partes
    const partes = dataString.split('-');
    const ano = parseInt(partes[0], 10);
    const mes = parseInt(partes[1], 10) - 1; // Meses são indexados de 0 a 11
    const dia = parseInt(partes[2], 10);

    // Cria um objeto Date com a hora definida para 00:00:00
    return new Date(ano, mes, dia, 0, 0, 0);
}
async function adicionarReserva(event) {
    event.preventDefault(); 
    const nome = document.getElementById("nome").value.trim();
    const quarto = document.getElementById("quarto").value.trim();
    let formapagamento = document.getElementById('pagamento');
    formapagamento = formapagamento.options[formapagamento.selectedIndex].text;
    const data1 = document.getElementById("data-checkin").value;
    const data2 = document.getElementById("data-checkout").value;
    let dataa = stringParaDate(data1)
    let datab = stringParaDate(data2)
    let diferenca = datab.getTime() - dataa.getTime()
    diferenca = Math.floor(diferenca/ (1000 * 60 * 60 *24))

    const response = await fetch('/reservar', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ nome, quarto, formapagamento, diferenca, data1, data2}),
    });

    const result = await response.json();
    const mensagem = document.getElementById("mensagem");

    if (response.ok) {
        window.location.href = result.redirect;
    } else {
        mensagem.textContent = "Erro ao reservar: " + result.message;
    }
    console.log(pagamento)
}

from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash, json

app = Flask(__name__, template_folder= 'Arquivos')
app.secret_key = 'chave ultra secreta'


class Usuario:
    def __init__(self, nome, endereco, cpf, telefone, email, senha):
        self.nome = nome
        self.endereco = endereco
        self.cpf = cpf
        self.telefone = telefone
        self.email = email
        self.senha = senha
        self.reservas = []
        self.total = 0

    def adiciona_reserva(self, reserva):
        self.reservas.append(reserva)
        
    def soma(self,n):
        self.total += n

class Reserva:
    def __init__(self, nome, quarto, pagamento, diferenca, data1, data2):
        self.nome = nome
        self.quarto = quarto
        self.pagamento = pagamento
        self.diferenca = diferenca
        self.data1 = data1
        self.data2 = data2

usuarios = []

def adicionar_usuario(nome, endereco, cpf, telefone, email, senha):
    if any(usuario.nome == nome for usuario in usuarios):
        return False  # Nome de usuário já existe
    novo_usuario = Usuario(nome, endereco, cpf, telefone, email, senha)
    usuarios.append(novo_usuario)
    return True

def adicionar_reserva_usuario(nome_usuario, reserva):
    usuario = next((usuario for usuario in usuarios if usuario.nome == nome_usuario), None)
    if usuario:
        usuario.adiciona_reserva(reserva)
        return True 
    return False  # Usuário não encontrado

def adicionar_total(nome_usuario, n):
    usuario = next((usuario for usuario in usuarios if usuario.nome == nome_usuario), None)
    if usuario:
        usuario.soma(n)
        return True 
    return False  # Usuário não encontrado

adicionar_usuario('admin', '', '', '', '', 'admin')
@app.route('/')
def inicio():
    return render_template('inicio.html')

@app.route('/cadastrar')
def cadastrar():
    return render_template('cadastro.html')

@app.route('/cadastro', methods=['POST'])
def cadastro():
    data = request.get_json()
    nome = data.get('nome')
    endereco = data.get('endereco')
    cpf = data.get('cpf')
    telefone = data.get('telefone')
    email = data.get('email')
    senha = data.get('senha')

    # Armazenar o usuário na lista
    adicionar_usuario(nome, endereco, cpf, telefone, email, senha)
    
    return jsonify({"redirect": "/login"}), 200

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if session.get('nome') is None:
        if request.method == 'POST':
            nome = request.form['nome']
            senha = request.form['senha']
            for usuario in usuarios:
                if usuario.nome == nome and usuario.senha == senha:
                    session['nome'] = nome
                    return redirect(url_for('inicio'))
        return render_template('login.html')
    else:
        flash('Você já está logado!')
        return redirect(url_for('inicio'))

@app.route('/reservar', methods=['POST'])
def reservar():
    data = request.get_json()
    nome = data.get('nome')
    quarto = data.get('quarto')
    pagamento = data.get('formapagamento')
    diferenca = data.get('diferenca')
    data1 = data.get('data1')
    data2 = data.get('data2')

    nova_reserva = Reserva(nome, quarto, pagamento, diferenca, data1, data2)
    adicionar_reserva_usuario(nome, nova_reserva)
    adicionar_total(nome, diferenca*300)

    return jsonify({"redirect": "/registros"}), 200

@app.route('/reservas')
def reservas():
    if session.get('nome') is None:
        flash("Você não está logado!")
        return redirect(url_for('inicio'))
    return render_template('reservas.html')

@app.route('/servicos')
def servicos():
    if session.get('nome') is None:
        flash("Você não está logado!")
        return redirect(url_for('inicio')) 
    usuario = next((usuario for usuario in usuarios if usuario.nome == session.get('nome')), None)
    if usuario:
        flash(f'Total: {usuario.total}')
    return render_template('servicos.html')

@app.route('/servicar', methods=['POST'])
def servicar():
    data = request.get_json()
    total = data['dados']['total']
    for usuario in usuarios:
        if usuario.nome == session.get('nome'):
            n = session.get('nome')
            adicionar_total(n, total)
    

    flash(f'Serviços selecionados! Custo total: R$ {total:.2f}')
    
    return jsonify({'redirect': '/servicos'}), 200
    

@app.route('/pagamentos')
def pagamentos():
    if session.get('nome') != 'admin':
        flash("Você não é adm!")
        return redirect(url_for('inicio'))
    return render_template('pagamentos.html', usuarios = usuarios)

@app.route('/pagar', methods=['POST'])
def pagar():
    print('PAGANDO')
    data = request.get_json()
    nome = data.get('nomeUsuario')
    for usuario in usuarios:
        if usuario.nome == nome:
            usuario.total = 0
            return jsonify({'redirect': '/pagamentos'}), 200


@app.route('/frigobar')
def frigobar():
    if session.get('nome') is None:
        flash("Você não está logado!")
        return redirect(url_for('inicio'))
    usuario = next((usuario for usuario in usuarios if usuario.nome == session.get('nome')), None)
    if usuario:
        flash(f'Total: R${usuario.total}')
    return render_template('frigobar.html')

@app.route('/frigobarar', methods=['POST'])
def frigobarar():
    data = request.get_json()
    total = data['dados']['total']
    for usuario in usuarios:
        if usuario.nome == session.get('nome'):
            n = session.get('nome')
            adicionar_total(n, total)
    

    flash(f'Serviços selecionados! Custo total: R$ {total:.2f}')
    
    return jsonify({'redirect': '/frigobar'}), 200

@app.route('/registros')
def registros():
    if session.get('nome') is None:
        flash("Você não está logado!")
        return redirect(url_for('inicio'))
    usuario = next((usuario for usuario in usuarios if usuario.nome == session.get('nome')), None)
    if usuario:
        return render_template('registro.html', reservas=usuario.reservas)
    
    flash("Usuário não encontrado.")
    return request(url_for('inicio'))

@app.route('/checkout')
def checkout():
    if session.get('nome') is None:
        flash("Você não está logado!")
        return redirect(url_for('inicio'))
    for usuario in usuarios:
        if usuario.nome == session.get('nome'): 
            if usuario.total == 0:
                return render_template('checkout.html', reservas=usuario.reservas, usuario=usuario)
            else:
                flash("Você não quitou suas dívidas!")
                return redirect(url_for('inicio'))

@app.route('/checkoutar', methods=['POST'])
def checkoutar():
    for usuario in usuarios:
        if usuario.nome == session.get('nome'):
            usuario.reservas = []
            return jsonify({'redirect': '/registros'}), 200
        

@app.route('/logout')
def logout():
    session.pop('nome', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
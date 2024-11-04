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
    def __init__(self, nome, quarto, pagamento, inicio, fim):
        self.nome = nome
        self.quarto = quarto
        self.pagamento = pagamento
        self.inicio = inicio
        self.fim = fim

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

for usuario in usuarios:
    total= 600
    adicionar_total('admin', total)
    for usuario in usuarios:
        if usuario.nome == 'admin':
            print(usuario.total)
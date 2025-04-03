from abc import ABC, abstractmethod
from datetime import datetime
import textwrap


class Cliente:
  def __init__(self, endereco):
    self.contas = []
    self.endereco = endereco
  
  def realizar_transacao(self, transacoes, conta):
    transacoes.registrar(conta)
  
  def adicionar_conta(self, conta):
    self.contas.append(conta)

class Pessoa_fisica(Cliente):
  def __init__(self, nome, cpf, endereco, data_nascimento):
    super().__init__(endereco)
    self.nome = nome
    self.cpf = cpf
    self.data_nascimento = data_nascimento

class Conta:
  def __init__(self, numero, cliente):
    self._saldo = 0
    self._numero = numero
    self._agencia = "0001"
    self._cliente = cliente
    self._historico = Historico()
  
  @classmethod
  def nova_conta(cls, cliente, numero):
    return cls(numero, cliente)
  
  @property
  def saldo(self):
    return self._saldo
  
  @property
  def numero(self):
    return self._numero
  
  @property
  def agencia(self):
    return self._agencia
  
  @property
  def cliente(self):
    return self._cliente
  
  @property
  def historico(self):
    return self._historico
  
  def sacar(self, valor):
    saldo = self.saldo
    excedeu_saldo = valor > saldo
    
    if saldo <= 0 or excedeu_saldo:
      print("Saldo insuficiente, faça um depósito")
    elif valor > 0:
      self._saldo -= valor
      print(f"Você sacou R${valor:.2f}")
      return True
    else:
      print("Erro ao sacar, digite um valor maior que 0")
    
    return False  
      
  def depositar(self, valor):
    if valor > 0:
      self._saldo += valor
      print(f"Você depositou R${valor:.2f}")
      return True      
    else:
      print("valor inválido, digite um valor maior que 0")
    return False

class Conta_corrente(Conta):
  def __init__(self, numero, cliente, limite=500, limite_saques=3):
    super().__init__(numero, cliente)
    self.limite = limite
    self.limite_saques = limite_saques
  
  def sacar(self, valor):
    numero_de_saques = len(
      [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]
    )
    excedeu_limite = valor > self.limite
    excedeu_limite_de_saques = numero_de_saques >= self.limite_saques
    
    if excedeu_limite:
      print("Você excedeu o limite de saque")
    elif excedeu_limite_de_saques:
      print("Você excedeu o limite de saques")
    else:
      super().sacar(valor)
      return True

    return False

  def __str__(self):
      return f"""\
        Agencia:\t {self.agencia}
        CC: \t\t {self.numero}
        Titular: \t {self.cliente.nome}
      """
               
class Historico:
  def __init__(self):
    self._transacoes = []
    
  @property
  def transacoes(self):
    return self._transacoes
  
  def adicionar_transacao(self, transacao):
    self._transacoes.append({
      "tipo": transacao.__class__.__name__,
      "valor": transacao.valor,
      "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    })
    
class Transacao(ABC):
  @property
  @abstractmethod
  def valor(self):
    pass
  @abstractmethod
  def registrar(self, conta):
    pass

class Saque(Transacao):
  def __init__(self, valor):
    self._valor = valor
    
  @property
  def valor(self):
    return self._valor
  
  def registrar(self, conta): 
    sucesso_transacao = conta.sacar(self.valor)
    if sucesso_transacao:
      conta.historico.adicionar_transacao(self)

class Deposito(Transacao):
  def __init__(self, valor):
    self._valor = valor

  @property
  def valor(self):
    return self._valor

  def registrar(self, conta):
    sucesso_transacao = conta.depositar(self.valor)
    if sucesso_transacao:
      conta.historico.adicionar_transacao(self)

def filtrar_cliente(cpf, clientes):
  clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
  return clientes_filtrados[0] if clientes_filtrados else None

def recuperar_conta_cliente(cliente):
  if not cliente.contas:
    print("conta não encontrada")
    return
  return cliente.contas[0]

def depositar(clientes):
  cpf = input("Digite o CPF do cliente: ")
  cliente = filtrar_cliente(cpf, clientes)
  if not cliente:
    print("Cliente não encontrado")
    return
  valor = float(input("Digite o valor do depósito: "))
  transacao = Deposito(valor)
  conta = recuperar_conta_cliente(cliente)
  if not conta:
    print("Conta não encontrada")
    return
  cliente.realizar_transacao(transacao, conta)

def sacar(clientes):
  cpf = input("Digite o CPF do cliente: ")
  cliente = filtrar_cliente(cpf, clientes)

  if not cliente:
    print("Cliente não encontrado")
    return
  valor = float(input("Digite o valor do saque: "))
  transacao = Saque(valor)
  conta = recuperar_conta_cliente(cliente)
  if not conta:
    print("Conta não encontrada")
    return
  cliente.realizar_transacao(transacao, conta)

def exibir_extrato(clientes):
  cpf = input("Digite o CPF do cliente: ")
  cliente = filtrar_cliente(cpf, clientes)
  if not cliente:
    print("Cliente não encontrado")
    return
  conta = recuperar_conta_cliente(cliente)
  if not conta:
    print("Conta não encontrada")
    return
  print("============ extrato ============")
  transacoes = conta.historico.transacoes
  
  extrato = ""
  if not transacoes: 
    extrato = "Nenhuma transação realizada"
  else: 
    for transacao in transacoes:
      extrato += f"\n {transacao['tipo']}: \t R$ {transacao['valor']:.2f} - {transacao['data']}\n"

  print(extrato)
  print(f"saldo atual: R$ {conta.saldo:.2f}")
  print("=================================")
  
def criar_cliente(clientes): 
  cpf = input("Digite o CPF do cliente: ")
  cliente = filtrar_cliente(cpf, clientes)
  if cliente:
    print("Cliente já cadastrado")
    return
  nome = input("Digite o nome do cliente: ")
  data_nascimento = input("Digite a data de nascimento do cliente: ")
  endereco = input("Digite o endereço ( Logradouro, N° - Bairro - Cidade/sigla - Estado): ")
  
  cliente = Pessoa_fisica(nome=nome, cpf=cpf, data_nascimento=data_nascimento, endereco=endereco)
  clientes.append(cliente)
  print("Cliente cadastrado com sucesso!")
  
def criar_conta(contas, clientes, numero_conta):
  cpf = input("Digite o CPF do cliente: ")
  cliente = filtrar_cliente(cpf, clientes)
  if not cliente:
    print("\n Cliente não encontrado")
    return
  conta = Conta_corrente.nova_conta(cliente=cliente, numero=numero_conta)
  contas.append(conta)
  cliente.contas.append(conta)
  print(f"Conta criada com sucesso!")
  
def listar_contas(contas):
  print("\n Contas cadastradas:")
  for conta in contas:
      print(textwrap.dedent(str(conta)))
      print("=================================")
  
def menu():  # Cria um menu para o usuário
    menu = '''\n
    -------- MENU --------
    Bem-vindo ao nosso Banco!!
    Escolha uma das opções abaixo:
    [nu] - Novo usuário
    [nc] - Criar conta
    [lc] - Listar contas
    [d] - Depósito
    [s] - Saque
    [e] - Extrato
    [sair] - Sair
    => '''
    return input(textwrap.dedent(menu))


def main():
  clientes = []
  contas = []
  
  while True:
    opcao = menu()
    
    if opcao == "d":
      depositar(clientes)
    elif opcao == "s":
      sacar(clientes)
    elif opcao == "e":
      exibir_extrato(clientes)
    elif opcao == "nu":
      criar_cliente(clientes)
    elif opcao == "nc":
      numero_conta = len(contas) + 1
      criar_conta(contas, clientes, numero_conta)
    elif opcao == "lc":
      listar_contas(contas)
    elif opcao == "sair":
      break
    else: 
      print("Opção inválida")
      
main()
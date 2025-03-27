from datetime import datetime



def menu(): # Cria um menu para o usuário
    print('''
    -------- MENU --------
    Bem-vindo ao nosso Banco!!
    Escolha uma das opções abaixo:
    [nc] - Novo usuário
    [cc] - Criar conta
    [lu] - Listar usuários
    [lc] - Listar contas
    [d] - Depósito
    [s] - Saque
    [e] - Extrato
    [sair] - Sair
    ''')

def client(clients): # Função para criar um novo cliente
  print("\n --- Novo Cliente ---")
  while True:
    cpf = input("Digíte seu CPF(somente numeros): ").strip()
    if cpf.isnumeric() and len(cpf) == 11:
      if any (c["cpf"] == cpf for c in clients):
        print("CPF já cadastrado! Digíte um CPF válido.")
        continue
      while True:
        name = input("Digíte seu nome: ")
        address = input("Digíte seu endereço {logradouro - N° - bairro - cidade - estado/sigla}: ")
        if name == "" or address == "":
          print("Nome e endereço são obrigatórios!")
          continue
        if name.isnumeric():
          print("Nome inválido! Digíte um nome válido.")
          continue
        break
      break
    else:
      print("CPF inválido! Digíte apenas números e com 11 digitos.") 
    
    
    
    
  while True:  
    birth_date = input("Digite sua data de nascimento(dd/mm/yyyy): ").strip()
    if len(birth_date) == 8 and birth_date.isnumeric():
      formatted_birth_date = f"{birth_date[:2]}/{birth_date[2:4]}/{birth_date[4:]}"
      try:
        datetime.strptime(formatted_birth_date, "%d/%m/%Y")
        break
      except ValueError:
        print("Data inválida! Digite no formato dd/mm/yyyy.")
        continue
    else:
      print("Data inválida! Digite apenas numeros e no formato dd-mm-yyyy.")
      
  print(f"\n Cliente {name} cadastrado com sucesso!\n")
  new_client = {
    "name": name.upper(),
    "cpf": cpf,
    "address": address.upper(),
    "birth_date": formatted_birth_date,
    "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

  clients.append(new_client)
  print("\n --- Cliente cadastrado com sucesso! ---\n")

def list_clients(clients): # Função para listar os clientes cadastrados
  print("\n --- Lista de Clientes ---")
  for client in clients:
    print(f'''
    ============================      
    
    nome: {client['name']}
    cpf: {client['cpf']} 
    endereço: {client['address']} 
    data de nascimento: {client['birth_date']}
    data de criação: {client['created_at']}
    '''
    )

def account(clients, accounts): # Função para criar uma conta
  print("\n --- Criar Conta ---")
  
  if not clients: 
    print("Não há clientes cadastrados! Cadastre um cliente primeiro.")
    return
  while True:  
    cpf = input("Digite o CPF do cliente: ").strip()
    
    client_data = next((c for c in clients if c["cpf"] == cpf), None)
    
    if client_data:
      new_account = {
        "client_cpf": client_data['cpf'], 
        "account_number": f"{len(accounts) + 1:04d}",  # Formata o número da conta como 4 dígitos, começando de 0001
        "client": client_data["name"],
        "agency": "0001",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
      }
      accounts.append(new_account)
      print(f"\nConta criada com sucesso para o cliente {client_data['name']}!\n")  
      break
    else:
      print("CPF não encontrado! Digite um CPF válido.")

def list_accounts(clients, accounts): # Função para listar as contas criadas
  print("\n --- Lista de Contas ---")
  while True:  
    print("\n Digite [sair] para voltar ao menu anterior.\n")
    if not accounts:
      print("Nenhuma conta cadastrada.")
      break
    cpf = input("Digite o CPF do cliente: ").strip()
    if cpf == "sair":  # Simplificado para verificar igualdade exata
      break  
    client_data = next((c for c in clients if c["cpf"] == cpf), None)
    if not client_data: 
      print("CPF não encontrado! Digite um CPF válido.")
      continue
    else:
      filtered_accounts = [account for account in accounts if account["client_cpf"] == cpf]
      for account in filtered_accounts:
        print(f'''
    ============================   
    nome: {client_data['name']}
    cpf: {client_data['cpf']}   
    número da conta: {account['account_number']}
    cliente: {account['client']} 
    agência: {account['agency']} 
    data de criação: {account['created_at']}
    '''
    )
      if not filtered_accounts:
        print("Nenhuma conta encontrada para este CPF.")

def deposit(balance, depositis): # Função para realizar um depósito
  print("\n --- Depósito ---")
  print("\n Digite [sair] para sair.\n")
  while True:
    deposit_input = input("Digite o valor do depósito: ").strip()
    if deposit_input.lower() == "sair":
      break
    try:
      deposit = float(deposit_input)
      if deposit <= 0:
        print("Valor inválido! Digite um valor positivo.")
        continue
      deposit_date_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
      balance += deposit

      depositis.append({"value": deposit, "created_at": deposit_date_time})
      print(f"O depósito no valor de R${deposit:.2f} realizado às {deposit_date_time}, foi depositado com sucesso!")
      print(f"Saldo atual: R${balance:.2f}")
      return balance
    except ValueError:
      print("Entrada inválida! Digite um valor numérico ou 'sair' para sair.")
     
      
def withdraw(* ,balance , withdrawals=None, limit = 500, max_withdral_per_day=3): # Função para realizar um saque
  print("\n --- Saque ---")
  print("\n Digite [sair] para sair.\n")
  while True:
    
    print(f"você tem um limite de {max_withdral_per_day} saques diários, no valor de R${limit:.2f}/saque. \n")
    if len(withdrawals) >= max_withdral_per_day:
      print(f"Limite de {max_withdral_per_day} saques diários atingido,  tente novamente amanhã!")
      break
    if len(withdrawals) == 2:
      print("Último saque disponivel hoje")
      withdraw_input = input("Digíte o valor do saque: ").strip()
    else: 
      print(f"Saques realizados hoje: {len(withdrawals)}")
      withdraw_input = input("Digíte o valor do saque: ").strip()
    
    if withdraw_input.lower() == "sair":
      break
    
    try:
      withdraw = float(withdraw_input)
      withdraw_date_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
      if withdraw > limit: 
        print(f"Seu limite é de R${limit:.2f} por saque!")
        continue
      elif withdraw <= 0:
        print("Valor inválido! Digite um valor positivo.")
        continue
      elif withdraw > balance:
        print("Saldo insuficiente!")
        continue
      
      balance -= withdraw
      withdrawals.append({"value": withdraw, "created_at": withdraw_date_time})
      print(f"Saque no valor de R${withdraw:.2f} feito ás {withdraw_date_time} foi realizado com sucesso!")
      print(f"Saldo atual: R${balance:.2f}")
      return balance 
    except ValueError:
      print("Entrada inválida! Digite um valor numérico ou 'sair' para sair.")
  
def  extract(balance, withdrawals, depositis ): # Função para exibir o extrato
  print("\n --- Extrato ---")
  if not depositis and not withdrawals:
    print("Nenhuma transação realizada.")
  else: 
    print("\n ============================ \n")
    if depositis:
      print(f"{len(depositis)} Depósito realizados:")
      for i, deposit in enumerate(depositis, start=1):
        print(f"   {i}. Depósito: R${deposit['value']:.2f} - {deposit['created_at']}\n")
      print("\n        ====================         \n")
    else:
      print("Nenhum depósito realizado.")
    if withdrawals:
      print(f"{len(withdrawals)} Saques realizados:")
      for i, withdraw in enumerate(withdrawals, start=1):
        print(f"   {i}. Saque: R${withdraw['value']:.2f} - {withdraw['created_at']} \n")
    else:
      print("Nenhum saque realizado.")  
    print("\n ============================ \n")
  print(f"Saldo atual: R${balance:.2f}")
  print("\n --- Fim do Extrato ---\n")
  
def bank_simulator(): # Função que irá permitir ao usuário realizar operações bancárias
  balance = 0
  withdrawals = []
  depositis = []
  clients = []
  accounts = []

  while True:
    menu() # Chamando a função menu para exibir as opções
    option = input("Digite uma opção: ").lower()
    if option not in ["nc", "cc", "lu", "lc", "d", "s", "e", "sair"]:
      print("\n Opção inválida! Digite uma das opções acima.\n")
      continue
    
    if option == "nc":  # Alterado para verificar igualdade exata
      client(clients)
    elif option == "cc":
      account(clients, accounts)
    elif option == "lu":
      list_clients(clients)
    elif option == "lc":
      list_accounts(clients, accounts)
    elif option == "d":
      balance = deposit(balance, depositis)
    elif option == "s":
      balance = withdraw(balance=balance, withdrawals=withdrawals)
    elif option == "e":
      extract(balance, withdrawals, depositis)   
    elif option == "sair":
      print("Obrigado por utilizar nosso Banco!")
      break
    
  
    
    
        
bank_simulator()
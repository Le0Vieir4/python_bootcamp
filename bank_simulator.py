balance = 0
depositis = []
withdrawals = []

def menu(): # Cria um menu para o usuário
    print('''
    -------- MENU --------
    Bem-vindo ao nosso Banco!!
    Escolha uma das opções abaixo:
    1 - Depósito
    2 - Saque
    3 - Extrato
    4 - Sair
    ''')

def bank_simulator(): # Função que ira permitit ao usuário realizar operações bancárias
  global balance # Variável global de saldo
  global deposits # Variável global de depósitos
  global withdrawals # Variável global de saques
  max_withdrawals_per_day = int(3) # Limite de saques por dia
  max_withdrawals_value_per_day = float(1500) # Limite do valor dos saques por dia
  
  while True:
    menu() # Chamando a funcão menu para exibir as opções
    
    try: # Tratamento de exceção para evitar erros ao usuario inserir uma str ou qualquer outro tipo de dado a nao ser int
        option = int(input("Digite a opção desejada: "))
    except ValueError:
        print("Opção inválida! Por favor, digite um número de 1 a 4.")
        continue  # Retorna ao início do loop
    
    if option < 1 or option > 4: # Verifica se a opção digitada é válida
        print("Opção inválida! Selecione uma opção de 1 a 4.")
   
    else:
      if option == 1:  # Depósito
        print(f"\n Seu saldo atual é de R${balance:.2f} \n")
        print("\n pressione 0 para voltar ao menu")
        
        try:
            print("Por favor digite o valor utilizando '.' para separar os centavos.")
            deposit = float(input("Digíte o valor do saque: "))
        except ValueError:
          print("Valor inválido! Tente novamente.")
          continue
        
        if deposit > 0: # Verifica se o valor do depósito é maior que 0
            balance += deposit # Adiciona o valor do depósito ao saldo
            depositis.append(deposit) # Adiciona o valor do depósito a lista de depósitos
            print(f"Depósito de R${deposit:.2f} efetuado com sucesso!")
        
        elif deposit == 0: # Verifica se o valor do depósito é igual a 0 e retorna ao menu
            menu()
        
        else: # Caso o valor do depósito seja menor que 0, exibe uma mensagem de erro
            print("Valor inválido! Tente novamente.")
            
      if option == 2: # saque
        print(f"\n Seu saldo atual é de R${balance:.2f} \n")
        print("pressione 0 para voltar ao menu\n")
        
        if len(withdrawals) > 2: # Verifica se o usuário atingiu o limite de saques diários
          print(f"Você atingiu o limite de saques diários!\n")
          
        else: 
          print(f"Você possuí um limite de {max_withdrawals_per_day} saques diários.\n")
          print(f"Você possuí um limite de R${max_withdrawals_value_per_day:.2f} em saques diários.")
          
          try:
            print("Por favor digite o valor utilizando '.' para separar os centavos.")
            withdrawal = float(input("Digíte o valor do saque: "))
          except ValueError:
            print("Valor inválido! Tente novamente.")
            continue
          
          if withdrawal > max_withdrawals_value_per_day: # Verifica se o valor do saque é maior que o limite diário
            print(f"seu limite de saque é de {max_withdrawals_value_per_day} por dia.")
          
          
          elif withdrawal > 500: # Verifica se o valor do saque é maior que o limite de saque
            print(f"\n Seu limite de saque é de R$500 por saque.\n")
            
          elif withdrawal < balance and withdrawal != 0: # Verifica se o valor do saque é menor ou igual ao saldo e diferente de 0
            balance -= withdrawal # Subtrai o valor do saque do saldo
            withdrawals.append(withdrawal) # Adiciona o valor do saque a lista de saques
            max_withdrawals_value_per_day -= withdrawal # Subtrai o valor do saque do limite diário
            max_withdrawals_per_day -= 1 # Subtrai 1 do limite de saques diários
            
            print(f"\n Saque de R${withdrawal:.2f} efetuado com sucesso!") 
              
          elif withdrawal > balance: # Verifica se o valor do saque é maior que o saldo
            print("Saldo insuficiente! Tente novamente.")
         
          if withdrawals == 0: # Verifica se o usuário digitou 0 e retorna ao menu
            menu()
          
          
      
      if option == 3:  # extrato
        print("\n --- extrato ---")
        print(f"\n você realizou: ")
        
        if depositis or withdrawals: # Verifica se o usuário realizou depósitos ou saques, se sim exibe a quantidade de depósitos e saques
          print(f"\n {len(depositis)}. depositos\n")
          print(f" {len(withdrawals)}. saques\n")
          
        else: # Caso o usuário não tenha realizado depósitos ou saques exibe a mensagem abaixo 
          print("\n 0. depositos")
          print("\n 0. saques\n")
          
        if depositis: # Verifica se o usuário realizou depósitos, se sim exibe os valores dos depósitos
          print("\n --- depositos --- \n")
          for i, valor in enumerate(depositis, 1):
            print(f"{i}. R${valor:.2f}")

      
        if withdrawals: # Verifica se o usuário realizou saques, se sim exibe os valores dos saques
          print("\n --- saques --- \n")        
          for i, valor in enumerate(withdrawals, 1):
            print(f"{i}. R${valor:.2f}")
        
        print("\n --- saldo --- \n")
        print(f"Seu saldo atual é de R${balance:.2f}\n") # Exibe o saldo atual do usuário

        if not depositis and not withdrawals: # Verifica se o usuário não realizou depósitos ou saques e exibe a mensagem abaixo
          print("Nenhuma operação realizada.")  
                
      elif option == 4:  # sair
        print("Obrigado por utilizar nosso banco!")
        break
    
    
        
bank_simulator()

# Funções

def interface():
    menu = """============== Operações Bancariás ==============

        [1] Depositar Dinheiro
        [2] Sacar Dinheiro
        [3] Exibir Extrato
        [4] Cadastrar Novo Usuário
        [5] Listar Usuários
        [6] Abrir Conta Corrente
        [7] Listar Contas
        [8] Sair

================================================"""
    op = input(f'{menu} \n=> ')
    return op

def logar_conta():
    pass

def depositar_valor(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito:\tR$ {valor:.2f}\n"
        print(f"\nDeposito do valor de R${valor:.2f} feito com sucesso!")

    else:
        print("\nOperação falhou! O valor informado é inválido.")

    return saldo, extrato

def sacar_valor(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print("\nOperação falhou! Você não tem saldo suficiente.")

    elif excedeu_limite:
        print("\nOperação falhou! O valor do saque excede o limite.")

    elif excedeu_saques:
        print("\nOperação falhou! Número máximo de saques excedido.")

    elif valor > 0:
        saldo -= valor
        extrato += f"Saque:\tR$ {valor:.2f}\n"
        numero_saques += 1
        print(f"\nSaque do valor de R${valor:.2f} feito com sucesso!")
        return saldo, extrato, numero_saques

    else:
        print("\nOperação falhou! O valor informado é inválido.")

def exibir_extrato(saldo, /, *, extrato):
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo:\tR$ {saldo:.2f}")
    print("==========================================")

def filtrar(lista, cpf):
    filtro = [item for item in lista if item['cpf'] == cpf]
    return filtro[0] if filtro else None

def cadastrar_usuario(usuarios, cpf):
    nome = input('Digite o nome completo do usuário:\n')
    
    if nome != '':
        nascimento = input('Digite a data de nascimento do usuário (dd/mm/yyyy):\n')

        if nascimento != '':
            endereco = input('Digite o endereço do usuario (logradouro, número - bairro - cidade/cigla estado):\n')

            if endereco != '':
                usuarios.append({'nome': nome, 'data_nascimento': nascimento, 'cpf': cpf, 'endereco': endereco})
                print(f"\nUsuário < {nome} > cadastrado com sucesso!")
            else:
                print('\nDigite um valor válido.')
                return
        else:
            print('\nDigite um valor válido.')
            return
    else:
        print('\nDigite um valor válido.')
        return

def listar_usuarios(usuarios):
    print(' Usuários Cadastrados '.center(70, '='))
    print(f'| {'Nome':<35} | {'CPF':<12} | {'Data de Nascimento':<18} | {'Endereço':<70} |')

    for usuario in usuarios:
        print(f'| {usuario['nome']:<35} | {usuario['cpf']:<12} | {usuario['data_nascimento']:<18} | {usuario['endereco']:<70} |')

def abrir_conta(contas, agencia, usuario):
    num_conta = len(contas) + 1
    contas.append({f'agencia': agencia, 'num_conta': num_conta, 'usuario': usuario})

    print(f'\nNova conta corrente de < {usuario['nome']} > criada com sucesso!')

def listar_contas(contas):
    print(' Contas Cadastradas '.center(70, '='))
    print(f'| {'agencia':<8} | {'num_conta':<10} | {'nome':<35} | {'cpf':<12} |')

    for conta in contas:
        print(f'| {conta['agencia']:<8} | {conta['num_conta']:<10} | {conta['usuario']['nome']:<35} | {conta['usuario']['cpf']:<12} |')

# Sistema

def main():
    LIMITE_SAQUES = 3
    AGENCIA = "0001"

    usuarios = []
    contas = []

    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    
    while True:
        opcao = interface()

        match opcao:
            case '1':
                valor = float(input("\nInforme o valor do depósito: "))

                saldo, extrato = depositar_valor(saldo, valor, extrato)

            case '2':
                valor = float(input("\nInforme o valor do saque: "))

                saldo, extrato, numero_saques = sacar_valor(
                    saldo=saldo,
                    valor=valor,
                    extrato=extrato,
                    limite=limite,
                    numero_saques=numero_saques,
                    limite_saques=LIMITE_SAQUES
                    )

            case '3':
                exibir_extrato(saldo, extrato=extrato)

            case '4':
                cpf = input('\nDigite o CPF do novo usuário (apenas números), ou digite "c" para cancelar:\n')

                if cpf != 'c':
                    if cpf != '':
                        if not filtrar(usuarios, cpf):
                            cadastrar_usuario(usuarios, cpf)
                        else:
                            print(f"\nUsuário com CPF < {cpf} > já cadastrado!")
                    else:
                        print('\nDigite um valor válido.')                        

            case '5':
                listar_usuarios(usuarios)

            case '6':
                if usuarios:
                    cpf = input('\nDigite o CPF para abrir a conta corrente (apenas números), ou digite "c" para cancelar:\n')

                    if cpf != 'c':
                        if cpf != '':
                            if filtrar(usuarios, cpf):
                                usuario = filtrar(usuarios, cpf)
                                abrir_conta(contas, AGENCIA, usuario) 
                            else:
                                print(f"\nConta com CPF < {cpf} > não encontrado!")
                        else:
                            print('\nDigite um valor válido.')     
                else:
                    print("\nNão há usuários cadastrados!")

            case '7':
                listar_contas(contas)

            case '8':
                print("\nFechando sistema...")
                break

            case _:
                print("\nOperação inválida, por favor selecione novamente a operação desejada.")

        input("\nTecle qualquer tecla para continuar...")

main()

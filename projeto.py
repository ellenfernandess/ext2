import sqlite3

# Função para criar conexão com o banco de dados SQLite
def conectar_banco_dados():
    """
    Conecta ao banco de dados SQLite e retorna o objeto de conexão.
    Se o banco de dados não existir, ele será criado automaticamente.
    """
    conexao = sqlite3.connect('gestao_empresarial.db')
    return conexao

# Função para criar as tabelas necessárias no banco de dados
def criar_tabelas(conexao):
    """
    Cria tabelas para o sistema de gestão:
    - produtos: para controlar o estoque.
    - vendas: para registrar as vendas realizadas.
    - clientes: para armazenar informações dos clientes.
    """
    cursor = conexao.cursor()
    # Criação da tabela de produtos
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS produtos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        preco REAL NOT NULL,
        quantidade INTEGER NOT NULL
    )
    ''')
    # Criação da tabela de vendas
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS vendas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        produto_id INTEGER NOT NULL,
        quantidade INTEGER NOT NULL,
        data_venda TEXT NOT NULL,
        valor_total REAL NOT NULL,
        FOREIGN KEY (produto_id) REFERENCES produtos(id)
    )
    ''')
    # Criação da tabela de clientes
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS clientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        email TEXT,
        telefone TEXT
    )
    ''')
    # Confirma a criação das tabelas
    conexao.commit()

# Função para adicionar um novo produto ao estoque
def adicionar_produto(conexao, nome, preco, quantidade):
    """
    Adiciona um novo produto ao banco de dados.
    :param conexao: conexão com o banco de dados.
    :param nome: nome do produto.
    :param preco: preço do produto.
    :param quantidade: quantidade em estoque do produto.
    """
    cursor = conexao.cursor()
    cursor.execute('''
    INSERT INTO produtos (nome, preco, quantidade)
    VALUES (?, ?, ?)
    ''', (nome, preco, quantidade))
    conexao.commit()

# Função para registrar uma nova venda
def registrar_venda(conexao, produto_id, quantidade, data_venda):
    """
    Registra uma nova venda no banco de dados.
    :param conexao: conexão com o banco de dados.
    :param produto_id: ID do produto vendido.
    :param quantidade: quantidade vendida.
    :param data_venda: data da venda.
    """
    cursor = conexao.cursor()
    # Verifica o estoque antes de registrar a venda
    cursor.execute('SELECT quantidade, preco FROM produtos WHERE id = ?', (produto_id,))
    produto = cursor.fetchone()
    if produto and produto[0] >= quantidade:
        valor_total = produto[1] * quantidade
        # Atualiza a quantidade no estoque
        cursor.execute('''
        UPDATE produtos
        SET quantidade = quantidade - ?
        WHERE id = ?
        ''', (quantidade, produto_id))
        # Insere a venda na tabela de vendas
        cursor.execute('''
        INSERT INTO vendas (produto_id, quantidade, data_venda, valor_total)
        VALUES (?, ?, ?, ?)
        ''', (produto_id, quantidade, data_venda, valor_total))
        conexao.commit()
        print("Venda registrada com sucesso!")
    else:
        print("Erro: Produto não encontrado ou quantidade insuficiente no estoque.")

# Função para visualizar todos os produtos no estoque
def visualizar_estoque(conexao):
    """
    Exibe todos os produtos e suas informações no banco de dados.
    :param conexao: conexão com o banco de dados.
    """
    cursor = conexao.cursor()
    cursor.execute('SELECT * FROM produtos')
    produtos = cursor.fetchall()
    print("Estoque atual:")
    for produto in produtos:
        print(f"ID: {produto[0]}, Nome: {produto[1]}, Preço: {produto[2]}, Quantidade: {produto[3]}")

# Função para visualizar todas as vendas registradas
def visualizar_vendas(conexao):
    """
    Exibe todas as vendas registradas no banco de dados.
    :param conexao: conexão com o banco de dados.
    """
    cursor = conexao.cursor()
    cursor.execute('''
    SELECT vendas.id, produtos.nome, vendas.quantidade, vendas.data_venda, vendas.valor_total
    FROM vendas
    JOIN produtos ON vendas.produto_id = produtos.id
    ''')
    vendas = cursor.fetchall()
    print("Vendas registradas:")
    for venda in vendas:
        print(f"ID: {venda[0]}, Produto: {venda[1]}, Quantidade: {venda[2]}, Data: {venda[3]}, Valor Total: {venda[4]}")

# Função principal para gerenciar o menu de interação com o usuário
def menu():
    """
    Menu principal para interação com o usuário, permitindo escolher ações
    como adicionar produtos, registrar vendas e visualizar dados.
    """
    conexao = conectar_banco_dados()
    criar_tabelas(conexao)

    while True:
        print("\nSistema de Gestão Empresarial")
        print("1. Adicionar Produto")
        print("2. Registrar Venda")
        print("3. Visualizar Estoque")
        print("4. Visualizar Vendas")
        print("5. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            nome = input("Nome do produto: ")
            preco = float(input("Preço do produto: "))
            quantidade = int(input("Quantidade em estoque: "))
            adicionar_produto(conexao, nome, preco, quantidade)
        elif opcao == '2':
            produto_id = int(input("ID do produto vendido: "))
            quantidade = int(input("Quantidade vendida: "))
            data_venda = input("Data da venda (YYYY-MM-DD): ")
            registrar_venda(conexao, produto_id, quantidade, data_venda)
        elif opcao == '3':
            visualizar_estoque(conexao)
        elif opcao == '4':
            visualizar_vendas(conexao)
        elif opcao == '5':
            conexao.close()
            break
        else:
            print("Opção inválida, por favor tente novamente.")

# Executa o menu principal
if __name__ == "__main__":
    menu()

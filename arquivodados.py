import sqlite3

def criar_banco():
    try:
        # Conectar ou criar o banco de dados
        conn = sqlite3.connect('BancoAtelier.db')
        cursor = conn.cursor()

        # Criar tabela CadastroClientes
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS CadastroClientes (
            ID_Cliente INTEGER PRIMARY KEY AUTOINCREMENT,
            Nome_cliente TEXT NOT NULL,
            Endereco TEXT,
            Cep TEXT,
            Cpf TEXT NOT NULL,
            Telefone TEXT
        )
        ''')

        # Criar tabela CadastroServicos com a coluna ID_Cliente
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS CadastroServicos (
            ID_Servico INTEGER PRIMARY KEY AUTOINCREMENT,
            Nome_projeto TEXT NOT NULL,
            Nome_cliente TEXT,
            Data_entrada DATE,
            Status TEXT CHECK(Status IN ('entrada', 'em andamento', 'terceirizado', 'vistoria', 'entregue')) NOT NULL,
            Detalhes TEXT,
            Quem_recebeu TEXT,
            Aprovacao TEXT,
            Data_entregue DATE,
            Quem_retirou TEXT,
            ID_Cliente INTEGER,
            FOREIGN KEY (ID_Cliente) REFERENCES CadastroClientes(ID_Cliente)
        )
        ''')

        # Salvar alterações e fechar conexão
        conn.commit()
        print("Banco de dados e tabelas criados/carregados com sucesso!")
    except sqlite3.Error as e:
        print(f"Erro ao criar banco de dados: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    criar_banco()

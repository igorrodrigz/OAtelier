import sqlite3

def testar_banco():
    conn = sqlite3.connect('BancoAtelier.db')
    cursor = conn.cursor()

    # Limpar tabelas antes dos testes
    cursor.execute("DELETE FROM CadastroClientes")
    cursor.execute("DELETE FROM CadastroServicos")

    # Inserir dados na tabela CadastroClientes
    clientes = [
        ('João Silva', 'Rua das Flores, 123', '12345-678', '123.456.789-00', '(11) 98765-4321'),
        ('Maria Oliveira', 'Av. Brasil, 456', '23456-789', '234.567.890-11', '(21) 12345-6789'),
        ('Carlos Souza', 'Rua dos Lírios, 789', '34567-890', '345.678.901-22', '(31) 23456-7890'),
        ('Ana Santos', 'Rua das Acácias, 101', '45678-901', '456.789.012-33', '(41) 34567-8901'),
        ('Fernanda Almeida', 'Av. das Palmeiras, 202', '56789-012', '567.890.123-44', '(51) 45678-9012'),
        ('Roberto Lima', 'Praça da Sé, 303', '67890-123', '678.901.234-55', '(61) 56789-0123'),
        ('Juliana Costa', 'Rua do Comércio, 404', '78901-234', '789.012.345-66', '(71) 67890-1234'),
        ('Marcelo Pereira', 'Av. Central, 505', '89012-345', '890.123.456-77', '(81) 78901-2345'),
        ('Patrícia Fernandes', 'Rua da Liberdade, 606', '90123-456', '901.234.567-88', '(91) 89012-3456'),
        ('Ricardo Rocha', 'Rua da Paz, 707', '01234-567', '012.345.678-99', '(11) 90123-4567')
    ]

    cursor.executemany('''
    INSERT INTO CadastroClientes (Nome_cliente, Endereco, Cep, Cpf, Telefone)
    VALUES (?, ?, ?, ?, ?)
    ''', clientes)

    # Inserir dados na tabela CadastroServicos
    servicos = [
        ('Projeto A', 'João Silva', '2024-01-10', 'entrada', 'Detalhes do Projeto A', 'Carlos', 'Aprovado', '2024-02-10', 'Ana', 1),
        ('Projeto B', 'Maria Oliveira', '2024-01-15', 'em andamento', 'Detalhes do Projeto B', 'Fernanda', 'Pendente', None, None, 2),
        ('Projeto C', 'Carlos Souza', '2024-02-05', 'vistoria', 'Detalhes do Projeto C', 'Roberto', 'Aprovado', '2024-03-15', 'Juliana', 3),
        ('Projeto D', 'Ana Santos', '2024-03-20', 'entrada', 'Detalhes do Projeto D', 'Marcelo', 'Pendente', None, None, 4),
        ('Projeto E', 'Fernanda Almeida', '2024-04-10', 'em andamento', 'Detalhes do Projeto E', 'Patrícia', 'Aprovado', '2024-05-01', 'Ricardo', 5),
        ('Projeto F', 'Roberto Lima', '2024-05-15', 'terceirizado', 'Detalhes do Projeto F', 'Carlos', 'Pendente', None, None, 6),
        ('Projeto G', 'Juliana Costa', '2024-06-01', 'entrada', 'Detalhes do Projeto G', 'Fernanda', 'Aprovado', '2024-06-15', 'Ana', 7),
        ('Projeto H', 'Marcelo Pereira', '2024-06-20', 'vistoria', 'Detalhes do Projeto H', 'Roberto', 'Pendente', None, None, 8),
        ('Projeto I', 'Patrícia Fernandes', '2024-07-05', 'em andamento', 'Detalhes do Projeto I', 'Marcelo', 'Aprovado', '2024-08-01', 'Ricardo', 9),
        ('Projeto J', 'Ricardo Rocha', '2024-08-15', 'entrada', 'Detalhes do Projeto J', 'Ana', 'Pendente', None, None, 10)
    ]

    cursor.executemany('''
    INSERT INTO CadastroServicos (Nome_projeto, Nome_cliente, Data_entrada, Status, Detalhes, Quem_recebeu, Aprovacao, Data_entregue, Quem_retirou, ID_Cliente)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', servicos)

    # Testar a consulta de clientes
    print("Clientes cadastrados:")
    cursor.execute("SELECT * FROM CadastroClientes")
    clientes = cursor.fetchall()
    for cliente in clientes:
        print(cliente)

    # Testar a consulta de serviços
    print("\nServiços cadastrados:")
    cursor.execute("SELECT * FROM CadastroServicos")
    servicos = cursor.fetchall()
    for servico in servicos:
        print(servico)

    # Testar atualização de dados
    print("\nAtualizando dados do Projeto A...")
    cursor.execute('''
    UPDATE CadastroServicos SET Status = 'entregue', Data_entregue = '2024-03-01' WHERE Nome_projeto = 'Projeto A'
    ''')
    conn.commit()

    # Testar exclusão de dados
    print("\nExcluindo dados do Projeto B...")
    cursor.execute('''
    DELETE FROM CadastroServicos WHERE Nome_projeto = 'Projeto B'
    ''')
    conn.commit()

    # Consultar novamente para verificar alterações
    print("\nServiços após atualização e exclusão:")
    cursor.execute("SELECT * FROM CadastroServicos")
    servicos_atualizados = cursor.fetchall()
    for servico in servicos_atualizados:
        print(servico)

    # Fechar a conexão
    conn.close()

if __name__ == '__main__':
    testar_banco()

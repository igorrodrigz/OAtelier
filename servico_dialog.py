import sqlite3
from PyQt5.QtWidgets import QDialog, QLineEdit, QFormLayout, QPushButton, QMessageBox, QComboBox, QDateEdit, QTextEdit
from PyQt5.QtCore import QDate

class ServicoDialog(QDialog):
    def __init__(self, parent=None, cliente_id=None, servico_id=None):
        super().__init__(parent)
        self.cliente_id = cliente_id
        self.servico_id = servico_id
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Adicionar Serviço")

        # Campos de entrada
        self.nome_projeto = QLineEdit()
        self.data_entrada = QDateEdit(calendarPopup=True)
        self.data_entrada.setDate(QDate.currentDate())
        self.data_prazo = QDateEdit(calendarPopup=True)
        self.status = QComboBox()
        self.status.addItems(['Entrada', 'Em Desenvolvimento','Testes','Periodo teste de versão','Alteração', 'Finalizado', 'Vistoria', 'Entregue'])
        self.detalhes = QTextEdit()
        self.material_adicional = QTextEdit()
        self.valor = QLineEdit()
        self.vendedor = QLineEdit()
        self.aprovacao = QLineEdit()
        self.data_entregue = QDateEdit(calendarPopup=True)
        self.quem_recebeu = QLineEdit()

        # Layout do formulário
        layout = QFormLayout()
        layout.addRow("Nome do Projeto:", self.nome_projeto)
        layout.addRow("Data de Entrada:", self.data_entrada)
        layout.addRow("Data Prazo:", self.data_prazo)
        layout.addRow("Status:", self.status)
        layout.addRow("Detalhes:", self.detalhes)
        layout.addRow("Material Adicional:", self.material_adicional)
        layout.addRow("Valor:", self.valor)
        layout.addRow("Vendedor:", self.vendedor)
        layout.addRow("Aprovação:", self.aprovacao)
        layout.addRow("Data Entregue:", self.data_entregue)
        layout.addRow("Quem Recebeu:", self.quem_recebeu)

        # Botão de salvar
        self.button_save = QPushButton("Salvar")
        self.button_save.clicked.connect(self.salvar_servico)

        layout.addWidget(self.button_save)
        self.setLayout(layout)

        # Carrega os dados se servico_id estiver definido
        if self.servico_id:
            self.carregar_dados()

    def carregar_dados(self):
        try:
            conexao = sqlite3.connect('BancoAtelier.db')
            cursor = conexao.cursor()
            cursor.execute(
                "SELECT Nome_projeto, Data_entrada, Data_prazo, Status, Detalhes, Material_adicional, Valor, Vendedor, Aprovacao, Data_entregue, Quem_recebeu FROM CadastroServicos WHERE ID_Servico = ?",
                (self.servico_id,))
            dados = cursor.fetchone()
            conexao.close()

            if dados:
                self.nome_projeto.setText(dados[0])
                self.data_entrada.setDate(QDate.fromString(dados[1], 'yyyy-MM-dd') if dados[1] else QDate.currentDate())
                self.data_prazo.setDate(QDate.fromString(dados[2], 'yyyy-MM-dd') if dados[2] else QDate.currentDate())
                self.status.setCurrentText(dados[3])
                self.detalhes.setPlainText(dados[4])
                self.material_adicional.setPlainText(dados[5])
                self.valor.setText(dados[6])
                self.vendedor.setText(dados[7])
                self.aprovacao.setText(dados[8])
                self.data_entregue.setDate(
                    QDate.fromString(dados[9], 'yyyy-MM-dd') if dados[9] else QDate.currentDate())
                self.quem_recebeu.setText(dados[10])
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Erro", f"Erro ao carregar dados do serviço: {e}")

    def salvar_servico(self):
        nome_projeto = self.nome_projeto.text()
        data_entrada = self.data_entrada.date().toString('yyyy-MM-dd')
        data_prazo = self.data_prazo.date().toString('yyyy-MM-dd')
        status = self.status.currentText()
        detalhes = self.detalhes.toPlainText()
        material_adicional = self.material_adicional.toPlainText()
        valor = self.valor.text()
        vendedor = self.vendedor.text()
        aprovacao = self.aprovacao.text()
        data_entregue = self.data_entregue.date().toString('yyyy-MM-dd')
        quem_recebeu = self.quem_recebeu.text()

        if not nome_projeto or not data_entrada or not status:
            QMessageBox.warning(self, "Aviso", "Preencha todos os campos obrigatórios.")
            return

        try:
            conexao = sqlite3.connect('BancoAtelier.db')
            cursor = conexao.cursor()

            if self.servico_id:
                cursor.execute("""
                    UPDATE CadastroServicos
                    SET Nome_projeto = ?, Data_entrada = ?, Data_prazo = ?, Status = ?, Detalhes = ?, Material_adicional = ?,
                     Valor = ?, Vendedor = ?, Aprovacao = ?, Data_entregue = ?, Quem_recebeu = ?
                    WHERE ID_Servico = ?
                """, (
                nome_projeto, data_entrada, data_prazo, status, detalhes, material_adicional, valor, vendedor, aprovacao, data_entregue, quem_recebeu,
                self.servico_id))
            else:
                cursor.execute("""
                    INSERT INTO CadastroServicos (Nome_projeto, Data_entrada, Data_prazo, Status, Detalhes, Material_adicional,
                     Valor, Vendedor, Aprovacao, Data_entregue, Quem_recebeu, ID_Cliente)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                nome_projeto, data_entrada, data_prazo, status, detalhes, material_adicional, valor, vendedor, aprovacao, data_entregue, quem_recebeu,
                self.cliente_id))

            conexao.commit()
            conexao.close()
            self.accept()
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Erro", f"Erro ao salvar serviço: {e}")


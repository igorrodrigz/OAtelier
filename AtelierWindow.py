import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QDialog, QFormLayout, QLineEdit, QLabel, QFrame
from PyQt5.QtCore import Qt
import sqlite3
from servicos_window import ServicosWindow

class ClientWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Atelier Recriar - Gestão de Clientes")
        self.setGeometry(100, 100, 1200, 800)

        # Layout principal
        main_layout = QVBoxLayout()

        # Frame 1: Campo de busca
        self.frame1 = QFrame()
        self.frame1.setFrameShape(QFrame.StyledPanel)
        frame1_layout = QHBoxLayout()
        self.search_field = QLineEdit()
        self.search_field.setPlaceholderText("Buscar cliente por nome, ID ou CPF")
        frame1_layout.addWidget(self.search_field)
        self.frame1.setLayout(frame1_layout)

        # Frame 2: Lista de clientes e Botões CRUD
        self.frame2 = QFrame()
        self.frame2.setFrameShape(QFrame.StyledPanel)
        frame2_layout = QHBoxLayout()

        # Frame 2.1: Lista de clientes
        self.frame2_1 = QFrame()
        self.frame2_1.setFrameShape(QFrame.StyledPanel)
        frame2_1_layout = QVBoxLayout()
        self.table_clientes = QTableWidget()
        self.table_clientes.setColumnCount(6)  # ID Cliente, Nome, Endereco, Cep, Cpf, Telefone
        self.table_clientes.setHorizontalHeaderLabels(
            ["ID", "Nome", "Endereço", "CEP", "CPF", "Telefone"]
        )
        self.table_clientes.setSelectionBehavior(QTableWidget.SelectRows)
        self.table_clientes.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table_clientes.cellDoubleClicked.connect(self.open_servicos_window)
        frame2_1_layout.addWidget(self.table_clientes)
        self.frame2_1.setLayout(frame2_1_layout)

        # Frame 2.2: Botões CRUD
        self.frame2_2 = QFrame()
        self.frame2_2.setFrameShape(QFrame.StyledPanel)
        frame2_2_layout = QVBoxLayout()
        self.button_add_cliente = QPushButton("Adicionar Cliente")
        self.button_edit_cliente = QPushButton("Editar Cliente")
        self.button_delete_cliente = QPushButton("Excluir Cliente")

        self.button_add_cliente.clicked.connect(self.adicionar_cliente)
        self.button_edit_cliente.clicked.connect(self.editar_cliente)
        self.button_delete_cliente.clicked.connect(self.excluir_cliente)

        frame2_2_layout.addWidget(self.button_add_cliente)
        frame2_2_layout.addWidget(self.button_edit_cliente)
        frame2_2_layout.addWidget(self.button_delete_cliente)
        self.frame2_2.setLayout(frame2_2_layout)

        frame2_layout.addWidget(self.frame2_1, 80)
        frame2_layout.addWidget(self.frame2_2, 20)
        self.frame2.setLayout(frame2_layout)

        # Frame 3: Informações adicionais
        self.frame3 = QFrame()
        self.frame3.setFrameShape(QFrame.StyledPanel)
        frame3_layout = QHBoxLayout()
        self.motivational_label = QLabel("Frase Motivacional Aqui")
        self.company_label = QLabel("<b>Atelier Recriar</b> - Desenvolvido por MR Solutions")
        frame3_layout.addWidget(self.motivational_label)
        frame3_layout.addWidget(self.company_label)
        self.frame3.setLayout(frame3_layout)

        # Adicionar frames ao layout principal
        main_layout.addWidget(self.frame1)
        main_layout.addWidget(self.frame2)
        main_layout.addWidget(self.frame3)

        self.setLayout(main_layout)
        self.load_clientes()

    def load_clientes(self):
        # Carregar clientes do banco de dados
        conn = sqlite3.connect('BancoAtelier.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM CadastroClientes")
        clientes = cursor.fetchall()
        self.table_clientes.setRowCount(len(clientes))
        for row_idx, cliente in enumerate(clientes):
            for col_idx, value in enumerate(cliente):
                item = QTableWidgetItem(str(value))
                self.table_clientes.setItem(row_idx, col_idx, item)
        conn.close()

    def adicionar_cliente(self):
        dialog = ClienteDialog(self)
        if dialog.exec_():
            self.load_clientes()

    def editar_cliente(self):
        selected_row = self.table_clientes.currentRow()
        if selected_row != -1:
            cliente_id_item = self.table_clientes.item(selected_row, 0)
            if cliente_id_item:
                cliente_id = cliente_id_item.text()
                dialog = ClienteDialog(self, cliente_id)
                if dialog.exec_():
                    self.load_clientes()

    def excluir_cliente(self):
        selected_row = self.table_clientes.currentRow()
        if selected_row != -1:
            cliente_id = self.table_clientes.item(selected_row, 0).text()
            conn = sqlite3.connect('BancoAtelier.db')
            cursor = conn.cursor()
            cursor.execute("DELETE FROM CadastroClientes WHERE ID_Cliente = ?", (cliente_id,))
            conn.commit()
            conn.close()
            self.load_clientes()

    def open_servicos_window(self, row, column):
        cliente_id = self.table_clientes.item(row, 0).text()
        self.servicos_window = ServicosWindow(cliente_id)
        self.servicos_window.exec_()

class ClienteDialog(QDialog):
    def __init__(self, parent=None, cliente_id=None):
        super().__init__(parent)
        self.cliente_id = cliente_id
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Adicionar Cliente" if not self.cliente_id else "Editar Cliente")
        layout = QFormLayout()

        self.input_nome = QLineEdit()
        self.input_endereco = QLineEdit()
        self.input_cep = QLineEdit()
        self.input_cpf = QLineEdit()
        self.input_telefone = QLineEdit()

        layout.addRow("Nome:", self.input_nome)
        layout.addRow("Endereço:", self.input_endereco)
        layout.addRow("CEP:", self.input_cep)
        layout.addRow("CPF:", self.input_cpf)
        layout.addRow("Telefone:", self.input_telefone)

        button_layout = QHBoxLayout()
        button_save = QPushButton("Salvar")
        button_cancel = QPushButton("Cancelar")

        button_save.clicked.connect(self.save)
        button_cancel.clicked.connect(self.reject)

        button_layout.addWidget(button_save)
        button_layout.addWidget(button_cancel)

        layout.addRow(button_layout)

        if self.cliente_id:
            self.load_cliente()

        self.setLayout(layout)

    def load_cliente(self):
        conn = sqlite3.connect('BancoAtelier.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM CadastroClientes WHERE ID_Cliente = ?", (self.cliente_id,))
        cliente = cursor.fetchone()
        if cliente:
            self.input_nome.setText(cliente[1])
            self.input_endereco.setText(cliente[2])
            self.input_cep.setText(cliente[3])
            self.input_cpf.setText(cliente[4])
            self.input_telefone.setText(cliente[5])
        conn.close()

    def save(self):
        nome = self.input_nome.text()
        endereco = self.input_endereco.text()
        cep = self.input_cep.text()
        cpf = self.input_cpf.text()
        telefone = self.input_telefone.text()

        conn = sqlite3.connect('BancoAtelier.db')
        cursor = conn.cursor()

        if self.cliente_id:
            cursor.execute('''UPDATE CadastroClientes SET Nome_cliente = ?, Endereco = ?, Cep = ?, Cpf = ?, Telefone = ? 
                              WHERE ID_Cliente = ?''', (nome, endereco, cep, cpf, telefone, self.cliente_id))
        else:
            cursor.execute('''INSERT INTO CadastroClientes (Nome_cliente, Endereco, Cep, Cpf, Telefone)
                              VALUES (?, ?, ?, ?, ?)''', (nome, endereco, cep, cpf, telefone))

        conn.commit()
        conn.close()
        self.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ClientWindow()
    window.show()
    sys.exit(app.exec_())

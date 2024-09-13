import sys
import sqlite3
import random
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, \
    QPushButton, QDialog, QFormLayout, QLineEdit, QLabel, QFrame, QSizePolicy, QSpacerItem, QMessageBox
from PyQt5.QtCore import Qt
from servicos_window import ServicosWindow


def carregar_estilos(app, caminho_qss):
    """Carrega os estilos do arquivo QSS no aplicativo."""
    with open(caminho_qss, "r") as arquivo_estilos:
        app.setStyleSheet(arquivo_estilos.read())


class ClientWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Atelier Recriar - Gestão de Clientes")
        self.setGeometry(100, 100, 1000, 600)

        # Layout principal
        main_layout = QVBoxLayout()

        # Frame 1: Campo de busca
        self.frame1 = QFrame(self)
        self.frame1.setObjectName("frame1")
        frame1_layout = QHBoxLayout()

        self.search_field = QLineEdit()
        self.search_field.setPlaceholderText("Buscar cliente por nome, ID ou CPF")
        self.search_button = QPushButton("Buscar")
        self.search_button.clicked.connect(self.buscar_cliente)

        frame1_layout.addWidget(self.search_field)
        frame1_layout.addWidget(self.search_button)
        self.frame1.setLayout(frame1_layout)

        # Frame 2: Lista de clientes e Botões CRUD
        self.frame2 = QFrame(self)
        frame2_layout = QHBoxLayout()

        # Frame 2.1: Lista de clientes
        self.frame2_1 = QFrame(self)
        self.frame2_1.setObjectName("frame2_1")
        frame2_1_layout = QVBoxLayout()
        self.table_clientes = QTableWidget()
        self.table_clientes.setColumnCount(6)
        self.table_clientes.setHorizontalHeaderLabels(["ID", "Nome", "Endereço", "CEP", "CPF", "Telefone"])
        self.table_clientes.setSelectionBehavior(QTableWidget.SelectRows)
        self.table_clientes.setEditTriggers(QTableWidget.NoEditTriggers)
        header = self.table_clientes.horizontalHeader()
        header.setFont(QFont("Arial", 12))
        frame2_1_layout.addWidget(self.table_clientes)
        self.frame2_1.setLayout(frame2_1_layout)

        # Frame 2.2: Botões CRUD e Acessar Cliente no painel lateral
        self.frame2_2 = QFrame(self)
        self.frame2_2.setObjectName("frame2_2")
        frame2_2_layout = QVBoxLayout()
        self.button_add_cliente = QPushButton("Adicionar Cliente")
        self.button_edit_cliente = QPushButton("Editar Cliente")
        self.button_delete_cliente = QPushButton("Excluir Cliente")
        self.button_access_cliente = QPushButton("Acessar Cliente")
        self.button_add_cliente.clicked.connect(self.adicionar_cliente)
        self.button_edit_cliente.clicked.connect(self.editar_cliente)
        self.button_delete_cliente.clicked.connect(self.excluir_cliente)
        self.button_access_cliente.clicked.connect(self.open_servicos_window)

        frame2_2_layout.addWidget(self.button_add_cliente)
        frame2_2_layout.addSpacerItem(QSpacerItem(2, 4, QSizePolicy.Minimum, QSizePolicy.Expanding))
        frame2_2_layout.addWidget(self.button_edit_cliente)
        frame2_2_layout.addSpacerItem(QSpacerItem(2, 4, QSizePolicy.Minimum, QSizePolicy.Expanding))
        frame2_2_layout.addWidget(self.button_delete_cliente)
        frame2_2_layout.addSpacerItem(QSpacerItem(2, 4, QSizePolicy.Minimum, QSizePolicy.Expanding))
        frame2_2_layout.addWidget(self.button_access_cliente)
        frame2_2_layout.addStretch()
        self.frame2_2.setLayout(frame2_2_layout)

        # Adicionar frames ao layout do Frame 2
        frame2_layout.addWidget(self.frame2_1, 80)
        frame2_layout.addWidget(self.frame2_2, 20)
        self.frame2.setLayout(frame2_layout)

        # Frame 3: Informações adicionais
        self.frame3 = QFrame(self)
        frame3_layout = QVBoxLayout()
        self.motivational_label = QLabel(self.get_motivational_quote())
        self.motivational_label.setFont(QFont("Arial", 16))
        self.motivational_label.setWordWrap(True)
        self.company_label = QLabel("<b>Software Exclusivo Atelier Recriar</b> - Desenvolvido por MR Solutions")
        frame3_layout.addWidget(self.motivational_label)
        frame3_layout.addWidget(self.company_label)
        self.frame3.setLayout(frame3_layout)

        # Adicionar frames ao layout principal
        main_layout.addWidget(self.frame1)
        main_layout.addWidget(self.frame2)
        main_layout.addWidget(self.frame3)

        self.setLayout(main_layout)
        self.load_clientes()

    def get_motivational_quote(self):
        """Retorna uma citação motivacional aleatória."""
        local_quotes = [
            "O sucesso é a soma de pequenos esforços repetidos dia após dia.",
            "Acredite em si mesmo e em tudo o que você é capaz de realizar.",
            "Cada dia é uma nova oportunidade para mudar sua vida.",
            "O fracasso é apenas a oportunidade de começar de novo com mais sabedoria.",
            "Não espere por oportunidades. Crie-as."
        ]
        return random.choice(local_quotes)

    def load_clientes(self):
        """Carrega os clientes do banco de dados na tabela."""
        try:
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
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao carregar clientes: {e}")

    def adicionar_cliente(self):
        """Abre o diálogo para adicionar um novo cliente."""
        dialog = ClienteDialog(self)
        if dialog.exec_():
            self.load_clientes()

    def editar_cliente(self):
        """Abre o diálogo para editar um cliente existente."""
        try:
            selected_row = self.table_clientes.currentRow()
            if selected_row != -1:
                cliente_id_item = self.table_clientes.item(selected_row, 0)
                if cliente_id_item:
                    cliente_id = cliente_id_item.text()
                    if cliente_id:
                        dialog = ClienteDialog(self, cliente_id)
                        if dialog.exec_():
                            self.load_clientes()
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao editar cliente: {e}")

    def excluir_cliente(self):
        """Exclui o cliente selecionado após confirmação."""
        selected_row = self.table_clientes.currentRow()
        if selected_row != -1:
            cliente_id = self.table_clientes.item(selected_row, 0).text()
            reply = QMessageBox.question(self, 'Confirmação de Exclusão',
                                         f'Tem certeza que deseja excluir o cliente com ID {cliente_id}?',
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                try:
                    conn = sqlite3.connect('BancoAtelier.db')
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM CadastroClientes WHERE ID_Cliente = ?", (cliente_id,))
                    conn.commit()
                    conn.close()
                    self.load_clientes()
                    QMessageBox.information(self, "Sucesso", "Cliente excluído com sucesso!")
                except Exception as e:
                    QMessageBox.critical(self, "Erro", f"Erro ao excluir cliente: {e}")

    def buscar_cliente(self):
        """Busca clientes com base no texto da pesquisa."""
        search_text = self.search_field.text()
        try:
            conn = sqlite3.connect('BancoAtelier.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM CadastroClientes WHERE Nome_cliente LIKE ? OR ID_Cliente LIKE ? OR Cpf LIKE ?",
                           (f"%{search_text}%", f"%{search_text}%", f"%{search_text}%"))
            clientes = cursor.fetchall()
            self.table_clientes.setRowCount(len(clientes))
            for row_idx, cliente in enumerate(clientes):
                for col_idx, value in enumerate(cliente):
                    item = QTableWidgetItem(str(value))
                    self.table_clientes.setItem(row_idx, col_idx, item)
            conn.close()
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao buscar clientes: {e}")

    def open_servicos_window(self):
        """Abre a janela de serviços para o cliente selecionado."""
        selected_row = self.table_clientes.currentRow()
        if selected_row != -1:
            cliente_id = self.table_clientes.item(selected_row, 0).text()
            self.servicos_window = ServicosWindow(cliente_id)
            self.servicos_window.show()


class ClienteDialog(QDialog):
    def __init__(self, parent=None, cliente_id=None):
        super().__init__(parent)
        self.cliente_id = cliente_id
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Adicionar/Editar Cliente")
        self.setGeometry(200, 200, 400, 300)
        layout = QFormLayout()

        self.nome_input = QLineEdit()
        self.endereco_input = QLineEdit()
        self.cep_input = QLineEdit()
        self.cpf_input = QLineEdit()
        self.telefone_input = QLineEdit()

        if self.cliente_id:
            self.load_cliente()
        else:
            self.setWindowTitle("Adicionar Cliente")

        layout.addRow(QLabel("Nome:"), self.nome_input)
        layout.addRow(QLabel("Endereço:"), self.endereco_input)
        layout.addRow(QLabel("CEP:"), self.cep_input)
        layout.addRow(QLabel("CPF:"), self.cpf_input)
        layout.addRow(QLabel("Telefone:"), self.telefone_input)

        button_layout = QHBoxLayout()
        self.save_button = QPushButton("Salvar")
        self.cancel_button = QPushButton("Cancelar")
        self.save_button.clicked.connect(self.save_cliente)
        self.cancel_button.clicked.connect(self.reject)

        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)

        layout.addRow(button_layout)

        self.setLayout(layout)

    def load_cliente(self):
        """Carrega as informações do cliente para edição."""
        try:
            conn = sqlite3.connect('BancoAtelier.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM CadastroClientes WHERE ID_Cliente = ?", (self.cliente_id,))
            cliente = cursor.fetchone()
            conn.close()
            if cliente:
                self.nome_input.setText(cliente[1])
                self.endereco_input.setText(cliente[2])
                self.cep_input.setText(cliente[3])
                self.cpf_input.setText(cliente[4])
                self.telefone_input.setText(cliente[5])
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao carregar cliente: {e}")

    def save_cliente(self):
        """Salva ou atualiza as informações do cliente no banco de dados."""
        nome = self.nome_input.text()
        endereco = self.endereco_input.text()
        cep = self.cep_input.text()
        cpf = self.cpf_input.text()
        telefone = self.telefone_input.text()

        if self.cliente_id:
            try:
                conn = sqlite3.connect('BancoAtelier.db')
                cursor = conn.cursor()
                cursor.execute("UPDATE CadastroClientes SET Nome_cliente = ?, Endereco = ?, Cep = ?, Cpf = ?, Telefone = ? WHERE ID_Cliente = ?",
                               (nome, endereco, cep, cpf, telefone, self.cliente_id))
                conn.commit()
                conn.close()
                QMessageBox.information(self, "Sucesso", "Cliente atualizado com sucesso!")
                self.accept()
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Erro ao atualizar cliente: {e}")
        else:
            try:
                conn = sqlite3.connect('BancoAtelier.db')
                cursor = conn.cursor()
                cursor.execute("INSERT INTO CadastroClientes (Nome_cliente, Endereco, Cep, Cpf, Telefone) VALUES (?, ?, ?, ?, ?)",
                               (nome, endereco, cep, cpf, telefone))
                conn.commit()
                conn.close()
                QMessageBox.information(self, "Sucesso", "Cliente adicionado com sucesso!")
                self.accept()
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Erro ao adicionar cliente: {e}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    carregar_estilos(app, "styles.qss")  # Certifique-se de que o caminho do arquivo QSS está correto
    window = ClientWindow()
    window.show()
    sys.exit(app.exec_())

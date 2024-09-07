import sys
from PyQt5.QtWidgets import (
    QApplication, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QDialog, QFormLayout, QLineEdit, QComboBox, QMessageBox, QLabel
)
from PyQt5.QtCore import Qt, QDate
from utils import criar_seletor_data
import sqlite3

class ServicosWindow(QDialog):
    def __init__(self, cliente_id, parent=None):
        super().__init__(parent)
        self.cliente_id = cliente_id
        self.cliente_nome = self.buscar_nome_cliente(self.cliente_id)
        self.initUI()

    def initUI(self):
        self.setWindowTitle(f"Serviços do Cliente {self.cliente_nome}")
        self.setGeometry(100, 100, 1100, 600)
        main_layout = QVBoxLayout()

        # Label para exibir o nome do cliente
        self.label_nome_cliente = QLabel(f"Nome do Cliente: {self.cliente_nome}")
        main_layout.addWidget(self.label_nome_cliente)

        # Tabela de serviços
        self.table_servicos = QTableWidget()
        self.table_servicos.setColumnCount(10)
        self.table_servicos.setHorizontalHeaderLabels([
            "ID Serviço", "Nome Projeto", "Nome Cliente", "Data Entrada", "Status", "Detalhes",
            "Quem Recebeu", "Aprovação", "Data Entregue", "Quem Retirou"
        ])
        self.table_servicos.setSelectionBehavior(QTableWidget.SelectRows)
        self.table_servicos.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table_servicos.cellDoubleClicked.connect(self.editar_servico)

        # Botões
        button_layout = QHBoxLayout()
        self.button_add_servico = QPushButton("Adicionar Serviço")
        self.button_edit_servico = QPushButton("Editar Serviço")
        self.button_delete_servico = QPushButton("Excluir Serviço")

        self.button_add_servico.clicked.connect(self.adicionar_servico)
        self.button_edit_servico.clicked.connect(self.editar_servico)
        self.button_delete_servico.clicked.connect(self.excluir_servico)

        button_layout.addWidget(self.button_add_servico)
        button_layout.addWidget(self.button_edit_servico)
        button_layout.addWidget(self.button_delete_servico)

        main_layout.addWidget(self.table_servicos)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)
        self.load_servicos()

    def buscar_nome_cliente(self, cliente_id):
        try:
            conn = sqlite3.connect('BancoAtelier.db')
            cursor = conn.cursor()
            cursor.execute("SELECT Nome_cliente FROM CadastroClientes WHERE ID_Cliente = ?", (cliente_id,))
            cliente = cursor.fetchone()
            conn.close()

            if cliente:
                return cliente[0]
            return "Cliente não encontrado"
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao buscar nome do cliente: {e}")
            return "Erro ao buscar cliente"

    def load_servicos(self):
        try:
            conn = sqlite3.connect('BancoAtelier.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM CadastroServicos WHERE ID_Cliente = ?", (self.cliente_id,))
            servicos = cursor.fetchall()
            self.table_servicos.setRowCount(len(servicos))

            for row_idx, servico in enumerate(servicos):
                for col_idx, value in enumerate(servico):
                    item = QTableWidgetItem(str(value))
                    self.table_servicos.setItem(row_idx, col_idx, item)

            conn.close()
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao carregar serviços: {e}")

    def adicionar_servico(self):
        dialog = ServicoDialog(self, self.cliente_id)
        if dialog.exec_():
            self.load_servicos()

    def editar_servico(self):
        selected_row = self.table_servicos.currentRow()
        if selected_row != -1:
            servico_id_item = self.table_servicos.item(selected_row, 0)
            if servico_id_item:
                servico_id = servico_id_item.text()
                dialog = ServicoDialog(self, self.cliente_id, servico_id)
                if dialog.exec_():
                    self.load_servicos()

    def excluir_servico(self):
        selected_row = self.table_servicos.currentRow()
        if selected_row != -1:
            servico_id = self.table_servicos.item(selected_row, 0).text()
            reply = QMessageBox.question(self, 'Confirmação', f"Tem certeza que deseja excluir o serviço ID {servico_id}?",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                try:
                    conn = sqlite3.connect('BancoAtelier.db')
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM CadastroServicos WHERE ID_Servico = ?", (servico_id,))
                    conn.commit()
                    conn.close()
                    self.load_servicos()
                except Exception as e:
                    QMessageBox.critical(self, "Erro", f"Erro ao excluir serviço: {e}")

class ServicoDialog(QDialog):
    def __init__(self, parent=None, cliente_id=None, servico_id=None):
        super().__init__(parent)
        self.cliente_id = cliente_id
        self.servico_id = servico_id
        self.cliente_nome = self.buscar_nome_cliente()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Adicionar Serviço" if not self.servico_id else "Editar Serviço")
        layout = QFormLayout()

        self.input_nome_projeto = QLineEdit()
        self.input_nome_cliente = QLineEdit()
        self.input_nome_cliente.setText(self.cliente_nome)
        self.input_nome_cliente.setReadOnly(True)
        self.input_data_entrada = criar_seletor_data()
        self.input_data_entregue = criar_seletor_data()
        self.input_status = QComboBox()
        self.input_status.addItems(["entrada", "em andamento", "terceirizado", "vistoria", "entregue"])
        self.input_detalhes = QLineEdit()
        self.input_quem_recebeu = QLineEdit()
        self.input_aprovacao = QLineEdit()
        self.input_quem_retirou = QLineEdit()

        layout.addRow("Nome Projeto:", self.input_nome_projeto)
        layout.addRow("Nome Cliente:", self.input_nome_cliente)
        layout.addRow("Data Entrada:", self.input_data_entrada)
        layout.addRow("Data Entregue:", self.input_data_entregue)
        layout.addRow("Status:", self.input_status)
        layout.addRow("Detalhes:", self.input_detalhes)
        layout.addRow("Quem Recebeu:", self.input_quem_recebeu)
        layout.addRow("Aprovação:", self.input_aprovacao)
        layout.addRow("Quem Retirou:", self.input_quem_retirou)

        button_layout = QHBoxLayout()
        button_save = QPushButton("Salvar")
        button_cancel = QPushButton("Cancelar")

        button_save.clicked.connect(self.save)
        button_cancel.clicked.connect(self.reject)

        button_layout.addWidget(button_save)
        button_layout.addWidget(button_cancel)

        layout.addRow(button_layout)

        if self.servico_id:
            self.load_servico()

        self.setLayout(layout)

    def buscar_nome_cliente(self):
        try:
            conn = sqlite3.connect('BancoAtelier.db')
            cursor = conn.cursor()
            cursor.execute("SELECT Nome_cliente FROM CadastroClientes WHERE ID_Cliente = ?", (self.cliente_id,))
            cliente = cursor.fetchone()
            conn.close()

            if cliente:
                return cliente[0]
            return "Cliente não encontrado"
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao buscar nome do cliente: {e}")
            return "Erro ao buscar cliente"

    def load_servico(self):
        try:
            conn = sqlite3.connect('BancoAtelier.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM CadastroServicos WHERE ID_Servico = ?", (self.servico_id,))
            servico = cursor.fetchone()
            if servico:
                self.input_nome_projeto.setText(servico[1])
                self.input_data_entrada.setDate(QDate.fromString(servico[3], 'yyyy-MM-dd') if servico[3] else QDate())
                self.input_status.setCurrentText(servico[4])
                self.input_detalhes.setText(servico[5])
                self.input_quem_recebeu.setText(servico[6])
                self.input_aprovacao.setText(servico[7])
                self.input_data_entregue.setDate(QDate.fromString(servico[8], 'yyyy-MM-dd') if servico[8] else QDate())
                self.input_quem_retirou.setText(servico[9])
            conn.close()
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao carregar serviço: {e}")

    def save(self):
        nome_projeto = self.input_nome_projeto.text().strip()
        data_entrada = self.input_data_entrada.date().toString('yyyy-MM-dd')
        status = self.input_status.currentText().strip()
        detalhes = self.input_detalhes.text().strip()
        quem_recebeu = self.input_quem_recebeu.text().strip()
        aprovacao = self.input_aprovacao.text().strip()
        data_entregue = self.input_data_entregue.date().toString('yyyy-MM-dd')
        quem_retirou = self.input_quem_retirou.text().strip()

        if not nome_projeto or not status:
            QMessageBox.warning(self, "Aviso", "Os campos 'Nome Projeto' e 'Status' são obrigatórios.")
            return

        try:
            conn = sqlite3.connect('BancoAtelier.db')
            cursor = conn.cursor()

            if self.servico_id:
                cursor.execute("""
                    UPDATE CadastroServicos
                    SET Nome_projeto = ?, Data_entrada = ?, Status = ?, Detalhes = ?, Quem_recebeu = ?, Aprovacao = ?, Data_entregue = ?, Quem_retirou = ?
                    WHERE ID_Servico = ?
                """, (nome_projeto, data_entrada, status, detalhes, quem_recebeu, aprovacao, data_entregue, quem_retirou, self.servico_id))
            else:
                cursor.execute("""
                    INSERT INTO CadastroServicos (ID_Cliente, Nome_projeto, Data_entrada, Status, Detalhes, Quem_recebeu, Aprovacao, Data_entregue, Quem_retirou)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (self.cliente_id, nome_projeto, data_entrada, status, detalhes, quem_recebeu, aprovacao, data_entregue, quem_retirou))

            conn.commit()
            conn.close()
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao salvar serviço: {e}")

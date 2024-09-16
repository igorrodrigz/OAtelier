import sys
from PyQt5.QtWidgets import (
    QApplication, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QDialog, QLabel, QFileDialog, QMessageBox
)
from PyQt5.QtCore import Qt
import sqlite3
import relatorio  # Importa o módulo de relatórios
from servico_dialog import ServicoDialog  # Importa o diálogo de serviços

class ServicosWindow(QDialog):
    def __init__(self, cliente_id, parent=None):
        super().__init__(parent)
        self.cliente_id = cliente_id
        self.cliente_nome = self.buscar_nome_cliente(self.cliente_id)
        self.initUI()

    def initUI(self):
        self.setWindowTitle(f"Serviços do Cliente {self.cliente_nome}")
        self.setGeometry(100, 100, 1000, 600)  # Ajuste o tamanho conforme necessário
        main_layout = QVBoxLayout()

        # Label para exibir o nome do cliente
        self.label_nome_cliente = QLabel(f"Nome do Cliente: {self.cliente_nome}")
        main_layout.addWidget(self.label_nome_cliente)

        # Tabela de serviços
        self.table_servicos = QTableWidget()
        self.table_servicos.setColumnCount(9)  # 9 colunas
        self.table_servicos.setHorizontalHeaderLabels([
            "ID Serviço", "Nome Projeto", "Data Entrada", "Status", "Detalhes",
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
        self.button_generate_report = QPushButton("Gerar Relatório")

        self.button_add_servico.clicked.connect(self.adicionar_servico)
        self.button_edit_servico.clicked.connect(self.editar_servico)
        self.button_delete_servico.clicked.connect(self.excluir_servico)
        self.button_generate_report.clicked.connect(self.gerar_relatorio)

        button_layout.addWidget(self.button_add_servico)
        button_layout.addWidget(self.button_edit_servico)
        button_layout.addWidget(self.button_delete_servico)
        button_layout.addWidget(self.button_generate_report)

        main_layout.addWidget(self.table_servicos)
        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

        self.load_servicos()

    def buscar_nome_cliente(self, cliente_id):
        """
        Obtém o nome do cliente a partir do banco de dados.
        """
        try:
            conexao = sqlite3.connect('BancoAtelier.db')
            cursor = conexao.cursor()
            cursor.execute("SELECT Nome_cliente FROM CadastroClientes WHERE ID_Cliente = ?", (cliente_id,))
            resultado = cursor.fetchone()
            conexao.close()
            if resultado:
                return resultado[0]
            else:
                return "Desconhecido"
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Erro", f"Erro ao conectar ao banco de dados: {e}")
            return "Desconhecido"

    def load_servicos(self):
        """
        Carrega os serviços do cliente na tabela.
        """
        try:
            conexao = sqlite3.connect('BancoAtelier.db')
            cursor = conexao.cursor()
            cursor.execute("""
            SELECT ID_Servico, Nome_projeto, Data_entrada, Status, Detalhes, Quem_recebeu, Aprovacao, Data_entregue, Quem_retirou
            FROM CadastroServicos
            WHERE ID_Cliente = ?
            """, (self.cliente_id,))
            servicos = cursor.fetchall()
            conexao.close()

            self.table_servicos.setRowCount(len(servicos))
            for row_idx, servico in enumerate(servicos):
                for col_idx, valor in enumerate(servico):
                    self.table_servicos.setItem(row_idx, col_idx, QTableWidgetItem(str(valor)))
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Erro", f"Erro ao carregar serviços: {e}")

    def adicionar_servico(self):
        try:
            # Passa o cliente_id corretamente ao instanciar o ServicoDialog
            dialog = ServicoDialog(self, self.cliente_id)
            if dialog.exec_() == QDialog.Accepted:
                self.load_servicos()  # Recarrega os serviços na tabela após a inserção
            else:
                QMessageBox.warning(self, "Aviso", "Erro ao abrir o diálogo de serviço.")
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao adicionar serviço: {e}")
            print(f"Erro ao adicionar serviço: {e}")
            self.load_servicos()

    def editar_servico(self):
        """
        Abre o diálogo para editar o serviço selecionado.
        """
        row = self.table_servicos.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Aviso", "Selecione um serviço para editar.")
            return

        id_servico = self.table_servicos.item(row, 0).text()

        try:
            # Passa o id_servico para o diálogo de edição
            dialog = ServicoDialog(self, servico_id=int(id_servico))
            if dialog.exec_() == QDialog.Accepted:
                self.load_servicos()
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao abrir o diálogo de serviço: {e}")

    def excluir_servico(self):
        """
        Exclui o serviço selecionado.
        """
        row = self.table_servicos.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Aviso", "Selecione um serviço para excluir.")
            return
        id_servico = self.table_servicos.item(row, 0).text()
        reply = QMessageBox.question(
            self, "Confirmação", "Tem certeza de que deseja excluir este serviço?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            try:
                conexao = sqlite3.connect('BancoAtelier.db')
                cursor = conexao.cursor()
                cursor.execute("DELETE FROM CadastroServicos WHERE ID_Servico = ?", (id_servico,))
                conexao.commit()
                conexao.close()
                self.load_servicos()
            except sqlite3.Error as e:
                QMessageBox.critical(self, "Erro", f"Erro ao excluir serviço: {e}")
                self.load_servicos()

    def gerar_relatorio(self):
        """
        Gera o relatório para os serviços do cliente.
        """
        # Verifica se alguma linha da tabela foi selecionada
        row = self.table_servicos.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Aviso", "Selecione um serviço para gerar o relatório.")
            return

        # Obtém o ID do serviço a partir da linha selecionada
        self.servico_id = self.table_servicos.item(row, 0).text()

        caminho_arquivo, _ = QFileDialog.getSaveFileName(self, "Salvar Relatório", "",
                                                         "PDF Files (*.pdf);;All Files (*)")
        if caminho_arquivo:
            try:
                # Obter os dados do serviço usando o ID do serviço
                servico = relatorio.obter_dados_servico(self.servico_id)
                if servico:
                    # Gera o relatório com os dados obtidos
                    relatorio.Relatorio.gerar_relatorio(servico, caminho_arquivo)
                    QMessageBox.information(self, "Sucesso", "Relatório gerado com sucesso!")
                else:
                    QMessageBox.warning(self, "Aviso", "Dados do serviço não encontrados.")
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Erro ao gerar relatório: {e}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ServicosWindow(cliente_id=1)  # Exemplo de ID do cliente
    window.show()
    sys.exit(app.exec_())

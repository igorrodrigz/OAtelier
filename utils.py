from PyQt5.QtWidgets import QDateEdit
from PyQt5.QtCore import QDate
import sqlite3
from contextlib import contextmanager

def criar_seletor_data(com_data_atual=False):
    """
    Cria um campo de seleção de data (QDateEdit) com um calendário popup.
    Por padrão, o campo começa vazio, mas pode ser configurado para começar com a data atual.

    Args:
        com_data_atual (bool): Se True, o campo de data começa com a data atual. Se False, o campo fica vazio.

    Returns:
        QDateEdit: Campo de seleção de data.
    """
    # Criar o campo de data com calendário popup
    date_edit = QDateEdit()
    date_edit.setDisplayFormat("dd/MM/yyyy")
    date_edit.setCalendarPopup(True)

    # Se o parâmetro com_data_atual for True, inicializar com a data atual
    if com_data_atual:
        date_edit.setDate(QDate.currentDate())
    else:
        # Deixar o campo de data vazio inicialmente
        date_edit.clear()

    # Definir ação para preencher a data atual se o campo estiver vazio quando for clicado
    def set_data_atual():
        if date_edit.date().isNull():
            date_edit.setDate(QDate.currentDate())

    # Conectar o foco ao evento de preencher com a data atual
    date_edit.editingFinished.connect(set_data_atual)

    return date_edit


@contextmanager
def get_db_connection():
    conn = sqlite3.connect('BancoAtelier.db')
    try:
        yield conn
    finally:
        conn.close()
import sqlite3
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
import logging
import os

# Configurar logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def obter_dados_servico(id_servico):
    """
    Obtém os dados do serviço a partir do banco de dados.
    """
    try:
        logging.debug(f"Tentando conectar ao banco de dados para obter o serviço com ID {id_servico}...")
        conexao = sqlite3.connect('BancoAtelier.db')
        cursor = conexao.cursor()

        query = """
        SELECT s.ID_Servico, s.Nome_projeto, c.Nome_cliente, s.Data_entrada, s.Status, s.Detalhes,
               s.Quem_recebeu, s.Aprovacao, s.Data_entregue, s.Quem_retirou
        FROM CadastroServicos s
        JOIN CadastroClientes c ON s.ID_Cliente = c.ID_Cliente
        WHERE s.ID_Servico = ?
        """
        cursor.execute(query, (id_servico,))
        dados_servico = cursor.fetchone()

        if dados_servico:
            logging.debug(f"Dados do serviço obtidos: {dados_servico}")
            return {
                'id_servico': dados_servico[0],
                'nome_projeto': dados_servico[1],
                'nome_cliente': dados_servico[2],
                'data_entrada': dados_servico[3],
                'status': dados_servico[4],
                'detalhes': dados_servico[5],
                'quem_recebeu': dados_servico[6],
                'aprovacao': dados_servico[7],
                'data_entregue': dados_servico[8],
                'quem_retirou': dados_servico[9]
            }
        else:
            logging.warning(f"Serviço com ID {id_servico} não encontrado.")
            return None

    except sqlite3.Error as e:
        logging.error(f"Erro ao conectar ao banco de dados: {e}")
        return None

class Relatorio:
    @staticmethod
    def gerar_relatorio(servico, caminho_arquivo):
        """
        Gera relatórios em PDF com base em um serviço.
        """
        try:
            if not servico:
                logging.warning("Dados do serviço estão incompletos ou inválidos.")
                return

            # Dados da empresa
            dados_empresa = {
                "Atelier Recriar": "Móveis Planejados • Restaurações • Antiguidades",
                "Endereço": "Rua Duque de Caxias, 2696, Uruguaiana - RS",
                "Telefone": "(55) 9 9971-8782 | (55) 3411-8923",
                "Redes Sociais": "@atelier.recriar"
            }

            # Caminho para o logotipo
            logo_path = 'logo2.png'

            # Configuração do documento PDF
            doc = SimpleDocTemplate(caminho_arquivo, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=60,
                                    bottomMargin=40)
            story = []

            # Estilos
            styles = getSampleStyleSheet()
            style_normal = styles['Normal']
            style_title = styles['Title']

            # Adicionar o logotipo se existir
            if os.path.exists(logo_path):
                logo = Image(logo_path)
                logo.drawWidth = 100  # Ajuste a largura conforme necessário
                logo.drawHeight = 100  # Ajuste a altura conforme necessário
                logo.hAlign = 'CENTER'
                story.append(logo)
                story.append(Spacer(1, 12))

            # Título do Relatório
            story.append(Paragraph("<b>Relatório de Serviços</b>", style_title))
            story.append(Spacer(1, 12))

            # Informações da Empresa
            for chave, valor in dados_empresa.items():
                story.append(Paragraph(f"<b>{chave}:</b> {valor}", style_normal))
            story.append(Spacer(1, 12))

            # Linha de separação
            story.append(Paragraph("<hr width='100%'/>", style_normal))
            story.append(Spacer(1, 12))

            # Título Detalhes do Serviço
            story.append(Paragraph("<b>Detalhes do Projeto</b>", style_title))
            story.append(Spacer(1, 12))

            # Detalhes do serviço como blocos de texto
            detalhes_servico = [
                ("ID Serviço", servico.get('id_servico', '')),
                ("Nome Projeto", servico.get('nome_projeto', '')),
                ("Nome Cliente", servico.get('nome_cliente', '')),
                ("Data Entrada", servico.get('data_entrada', '')),
                ("Status", servico.get('status', '')),
                ("Detalhes", servico.get('detalhes', '')),
                ("Quem Recebeu", servico.get('quem_recebeu', '')),
                ("Aprovação", servico.get('aprovacao', '')),
                ("Data Entregue", servico.get('data_entregue', '')),
                ("Quem Retirou", servico.get('quem_retirou', ''))
            ]

            for chave, valor in detalhes_servico:
                story.append(Paragraph(f"<b>{chave}:</b> {valor}", style_normal))
                story.append(Spacer(1, 8))

            # Gerar o PDF
            doc.build(story)
            logging.info(f"PDF gerado com sucesso em: {caminho_arquivo}")

        except Exception as e:
            logging.error(f"Erro ao gerar o relatório: {e}")

# Exemplo de uso
if __name__ == '__main__':
    id_servico = 26  # Substitua pelo ID do serviço desejado
    servico = obter_dados_servico(id_servico)  # Recupera os dados do serviço com o ID fornecido
    if servico:
        Relatorio.gerar_relatorio(servico, "relatorio_servico.pdf")  # Gera o relatório para o serviço selecionado
    else:
        logging.error("Não foi possível gerar o relatório: dados do serviço não encontrados.")

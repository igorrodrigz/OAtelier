# Atelier Recriar

**Atelier Recriar** é um software de gestão de serviços desenvolvido para empresas de móveis planejados e restauração. Ele permite gerenciar serviços, gerar relatórios e manter um controle eficiente das atividades da empresa.

## Funcionalidades

- Adicionar, editar e excluir serviços.
- Gerar relatórios em PDF para serviços específicos.
- Visualizar informações detalhadas dos serviços.

## Requisitos

- **Sistema Operacional**: Windows, macOS, ou Linux.
- **Python**: Versão 3.6 ou superior.
- **Dependências**:
  - PyQt5
  - SQLite3
  - PyInstaller

## Instalação

### 1. Clonar o Repositório

Clone o repositório para o seu ambiente local:
```bash
git clone https://github.com/seuusuario/atelier-recriar.git
cd atelier-recriar
2. Instalar Dependências
Instale as bibliotecas necessárias:

bash
Copiar código
pip install -r requirements.txt
Nota: Certifique-se de ter o Python 3.6 ou superior instalado.

3. Configuração do Banco de Dados
Certifique-se de que o banco de dados BancoAtelier.db está no diretório principal do projeto. Se não tiver, você pode criar o banco de dados e as tabelas necessárias conforme descrito no manual de instruções.

Uso
Iniciando o Software
Execute o arquivo executável gerado (por exemplo, AtelierWindow.exe para Windows):

bash
Copiar código
./AtelierWindow.exe
Tela Principal
Adicionar Serviço: Clique no botão "Adicionar Serviço" e preencha os dados no diálogo.
Editar Serviço: Selecione um serviço e clique em "Editar Serviço".
Excluir Serviço: Selecione um serviço e clique em "Excluir Serviço".
Gerar Relatório: Selecione um serviço e clique em "Gerar Relatório" para salvar um PDF com os detalhes do serviço.
Solução de Problemas
Erro ao Conectar ao Banco de Dados: Verifique se o arquivo BancoAtelier.db está no diretório correto e acessível.
Problemas com Relatórios: Certifique-se de ter selecionado um serviço e verifique o caminho de salvamento do relatório.
Atualizações e Suporte
Para atualizações e suporte, entre em contato com o desenvolvedor:

Email: suporte@atelierrecriar.com
Telefone: (55) 3412-0000
Contribuindo
Se você deseja contribuir para o projeto, por favor, faça um fork do repositório e envie um pull request com suas alterações.

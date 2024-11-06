# Sistema de Empréstimos de Livros

Este é um sistema simples desenvolvido em Django para gerenciar empréstimos de livros em uma biblioteca. O sistema possui dois tipos de usuários: **Leitores** e **Administradores**, com funcionalidades distintas para cada tipo de acesso.

## Funcionalidades

### Leitor:
- **Lista de Empréstimos**: Visualiza os empréstimos realizados.
- **Solicitar Empréstimo**: O usuário pode solicitar um empréstimo de livro disponível.
- **Visualizar Livros Disponíveis**: O usuário pode consultar a lista de livros disponíveis para empréstimo.
- **Filtrar por Nome**: O usuário pode filtrar os livros disponíveis por nome.

### Administrador:
- **Relatório por Clientes**: O administrador pode gerar relatórios de empréstimos por usuário.
- **Relatório Geral de Exemplares (Por Período)**: O administrador pode gerar um relatório sobre os livros emprestados em determinado período.
- **Gerenciar Livros, Empréstimos e Usuários**: O administrador tem a capacidade de adicionar, editar ou excluir livros, além de gerenciar os empréstimos e usuários.

## Tecnologias Utilizadas

- **Django**: Framework web utilizado para o desenvolvimento do sistema.
- **SQLite**: Banco de dados padrão para o desenvolvimento. --  USEI O POSTGREES
- **Bootstrap 4**: Framework CSS para o layout e design responsivo.
- **Font Awesome**: Ícones para a interface de usuário.

## Como Iniciar o Projeto

### 1. Clonar o Repositório

Clone o repositório para sua máquina local:

```bash
git clone https://github.com/seu-usuario/sistema-emprestimos.git
cd sistema-emprestimos


#2. Instalar as Dependências
Instale as dependências do projeto usando o pip:

bash
Copiar código
pip install -r requirements.txt
3. Configurar o Banco de Dados
O Django utiliza SQLite por padrão, então basta rodar as migrações para configurar o banco de dados:

bash
Copiar código
python manage.py migrate
4. Criar um Superusuário
Para acessar a área administrativa, você precisa criar um superusuário:

bash
Copiar código
python manage.py createsuperuser
Siga as instruções para definir o nome de usuário, e-mail e senha para o superusuário.

5. Rodar o Servidor de Desenvolvimento
Inicie o servidor de desenvolvimento:

bash
Copiar código
python manage.py runserver
Acesse a aplicação no seu navegador em http://127.0.0.1:8000.

O painel administrativo pode ser acessado em http://127.0.0.1:8000/admin, onde você pode gerenciar livros, empréstimos e usuários.
6. Acessando a Aplicação
Leitor: Pode acessar a página de livros disponíveis e realizar empréstimos.
Administrador: Pode acessar a página administrativa para gerenciar livros, usuários e gerar relatórios.
Estrutura do Projeto
bash
Copiar código
sistema-emprestimos/
│
├── manage.py                    # Script principal para gerenciar o Django
├── sistema_emprestimos/          # Diretório do projeto Django
│   ├── __init__.py
│   ├── settings.py               # Arquivo de configurações do Django
│   ├── urls.py                   # Definição das URLs do projeto
│   ├── wsgi.py
│   └── asgi.py
│
├── livros/                       # Aplicação para gerenciar livros e empréstimos
│   ├── __init__.py
│   ├── admin.py                  # Configuração do painel administrativo
│   ├── models.py                 # Modelos de dados (Livros, Empréstimos, etc)
│   ├── views.py                  # Lógica das views para exibir informações
│   ├── urls.py                   # URLs específicas da aplicação livros
│   └── migrations/               # Diretório de migrações
│
├── templates/                    # Arquivos HTML do projeto
│   ├── livros/                   # Templates específicos da aplicação livros
│   │   └── lista_livros.html     # Template para listar livros
│   └── outros_templates/
│
├── requirements.txt              # Dependências do projeto
└── db.sqlite3                    # Banco de dados SQLite (padrão)
Como Contribuir
Se você quiser contribuir para este projeto, siga as etapas abaixo:

Faça o fork deste repositório.
Crie uma branch para sua feature (git checkout -b feature/nova-feature).
Faça as alterações desejadas e envie para o seu repositório (git push origin feature/nova-feature).
Abra um pull request para o repositório original.
Licença
Este projeto é licenciado sob a Licença MIT - veja o arquivo LICENSE para mais detalhes.
Blog - Projeto Django
Este é um projeto de blog desenvolvido utilizando o framework Django. O objetivo principal é criar uma plataforma onde os usuários possam interagir com posts, curtir, comentar, seguir outros usuários e gerenciar seu perfil. O sistema inclui funcionalidades de gestão de tags, permitindo a categorização de posts de forma flexível.

Funcionalidades
Usuário
Cadastro de usuários, com informações como nome, email, senha, foto de perfil, data de nascimento, música favorita e biografia.
Edição do perfil, incluindo foto de capa, biografia e preferências.
Lista de seguidores e usuários seguidos.
Função de seguir e deixar de seguir outros usuários.
Posts
Criação, leitura e listagem de posts.
Funcionalidade de curtir posts, com a visualização das curtidas no perfil do usuário.
Exibição do autor do post com a possibilidade de visualizar o perfil do autor.
Tags
Criação, edição e exclusão de tags.
Atribuição de tags aos posts para categorização.
Exibição das tags no painel de configurações.
Administração
Interface administrativa para gerenciar usuários, posts e tags.
Funcionalidades Adicionais
Responsividade, garantindo que a página seja bem exibida em dispositivos móveis e desktops.
Estilos personalizados com animações e efeitos visuais para botões e interações.
Sistema de mensagens de erro e sucesso para ações realizadas no sistema.
Tecnologias Utilizadas
Django: Framework web para a criação da aplicação.
HTML/CSS: Estrutura e estilo das páginas.
Bootstrap: Framework para responsividade (caso seja utilizado).
JavaScript: Funcionalidades de interação adicionais (caso seja necessário).
SQLite: Banco de dados utilizado por padrão no Django (pode ser alterado para outros bancos como MySQL ou PostgreSQL).
Configuração do Projeto
Pré-requisitos
Python 3.x
Django 4.x
Biblioteca django-crispy-forms para facilitar a renderização dos formulários.
Instalação
Clone este repositório para o seu ambiente local:

bash
Copiar código
git clone https://github.com/seu-usuario/seu-projeto-blog.git
Navegue até o diretório do projeto:

bash
Copiar código
cd seu-projeto-blog
Crie um ambiente virtual:

bash
Copiar código
python -m venv venv
Ative o ambiente virtual:

Windows:

bash
Copiar código
venv\Scripts\activate
Mac/Linux:

bash
Copiar código
source venv/bin/activate
Instale as dependências:

bash
Copiar código
pip install -r requirements.txt
Faça as migrações do banco de dados:

bash
Copiar código
python manage.py migrate
Crie um superusuário para acessar o painel administrativo (opcional):

bash
Copiar código
python manage.py createsuperuser
Execute o servidor de desenvolvimento:

bash
Copiar código
python manage.py runserver
Acesse o aplicativo em http://127.0.0.1:8000.

Dependências
Django
crispy-forms
Estrutura de Diretórios
php
Copiar código
seu-projeto-blog/
│
├── blog/                  # Aplicação principal do blog
│   ├── migrations/        # Arquivos de migração do banco de dados
│   ├── templates/         # Templates HTML
│   ├── static/            # Arquivos estáticos (CSS, JS, imagens)
│   ├── models.py          # Modelos de dados (Usuários, Posts, Tags)
│   ├── views.py           # Lógica das views
│   └── urls.py            # Roteamento de URLs
│
├── manage.py              # Script para executar comandos de administração
├── requirements.txt       # Arquivo com as dependências do projeto
└── settings.py            # Configurações do Django
Como Contribuir
Faça um fork deste repositório.
Crie uma nova branch para sua feature (git checkout -b feature/feature-name).
Faça as alterações e commit (git commit -am 'Adiciona nova feature').
Envie para a branch do seu fork (git push origin feature/feature-name).
Crie um pull request com a descrição detalhada da feature.
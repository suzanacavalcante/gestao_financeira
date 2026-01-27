# 💰 Sistema de Gestão Financeira

> **Status do Projeto:**  🚧 Em desenvolvimento

## Sobre o Projeto

Este é um projeto de gestão financeira desenvolvido em **Python (Django)**, utilizando **PostgreSQL** como banco de dados e **Docker** para orquestração de ambiente. O projeto inclui dashboards para visualização de gastos e metas.

## Últimas Novidades
> O PROJETO JÁ POSSUI UMA V1
- **Arquitetura Dockerizada**: Aplicação e Banco de Dados (PostgreSQL) rodando em containers independentes.
- **Deploy em VPS**: Configurado para rodar em ambientes de produção.
- **Segurança**: Logout via POST e proteção de hosts configurada.
- **Estáticos Otimizados**: Uso do WhiteNoise para servir CSS/JS de forma eficiente em produção.

**Link para visualização:** [Acesse aqui o projeto]([PROJETO AINDA EM DESENVOLVIMENTO])

## Tecnologias Utilizadas

- **Backend**: Django 5.x
- **Banco de Dados**: PostgreSQL 16
- **Containerização**: Docker & Docker Compose
- **Frontend**: Bootstrap 5 & Bootstrap Icons
- **Servidor de Estáticos**: WhiteNoise

## Funcionalidades

- [x] **Design Responsivo:** Adaptado para dispositivos móveis, tablets e desktop.
- [x] **Tela de Login/Cadastroo:** O sistema permite cadastro, login e logout. As senhas são criptografadas.
- [x] **Lançamentos Financeiros:** O usuário pode registrar entradas (receitas) e saídas (despesas) com valor, data e descrição.
- [x] **Categoria** O usuário pode criar e editar categorias para classificar seus gastos.
- [x] **Gestão de Metas** Uma seção para definir objetivos financeiros com valor alvo e valor já poupado.
- [x] **Dashboard** Visualização gráfica de gastos por categoria, evolução mensal e status das metas.

## Estrutura do Projeto

* `web/`: Container contendo a aplicação Django.
* `db/`: Container do banco de dados PostgreSQL.
* `.env`: Arquivo de variáveis de ambiente (não versionado por segurança).
* `docker-compose.yml`: Configuração dos serviços.

## Como rodar o projeto

### 1. Pré-requisitos
Certifique-se de ter instalado em sua máquina ou VPS:
* Docker
* Docker Compose

### 2. Configuração do Ambiente
Crie um arquivo `.env` na raiz do projeto baseado nas variáveis necessárias:
```env
POSTGRES_DB=financas_db
POSTGRES_USER=[TENHA SEU PRÓPRIO USUÁRIO]
POSTGRES_PASSWORD=[TENHA SUA PRÓPRIA SENHA]
SECRET_KEY=[TENHA SUA PRÓPRIA SENHA]
DEBUG=1
```

### 3. Configuração Inicial
```bash
# Construir e subir os containers
docker-compose up -d --build

# Executar as migrações do banco de dados
docker-compose exec [nome_projeto] python manage.py migrate

# Criar um usuário administrador
docker-compose exec [nome_projeto] python manage.py createsuperuser
```
O sistema estará disponível em: http://localhost:8000 (ou o IP do seu servidor).

## Estrutura de Volumes
O projeto utiliza volumes persistentes para garantir que seus dados não sejam perdidos ao reiniciar os containers:

- ./djangoapp: Código fonte da aplicação.
- ./data/web/static: Arquivos estáticos servidos.
- ./data/postgres/data: Dados persistentes do PostgreSQL.

## Comandos Úteis
- Ver logs: docker-compose logs -f djangoapp
- Reiniciar serviços: docker-compose restart
- Derrubar tudo: docker-compose down

## Segurança
- **Gestão de Credenciais**: Uso de variáveis de ambiente (`.env`) e hashes de senha PBKDF2.
- **Middleware de Proteção**: Defesa nativa contra ataques CSRF, XSS e SQL Injection.
- **Isolamento de Infraestrutura**: Database isolado em rede Docker privada e execução do app com usuário de sistema limitado (`non-root`).
- **Proteção de Host**: Filtro de requisições via `ALLOWED_HOSTS` para evitar ataques de envenenamento de cabeçalho HTTP.

Desenvolvido por Suzana Cavalcante

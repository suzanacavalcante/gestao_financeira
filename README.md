# 💰 Sistema de Gestão Financeira

> **Status do Projeto:**  🚧 Em desenvolvimento

## 💻 Sobre o Projeto

Este é um projeto de gestão financeira desenvolvido em **Python (Django)**, utilizando **PostgreSQL** como banco de dados e **Docker** para orquestração de ambiente. O projeto inclui dashboards para visualização de gastos e metas.

**Link para visualização:** [Acesse aqui o projeto]([PROJETO AINDA EM DESENVOLVIMENTO])

## 🚀 Tecnologias Utilizadas

* **Linguagem:** Python 3.11
* **Framework Web:** Django
* **Banco de Dados:** PostgreSQL 15
* **Containerização:** Docker & Docker Compose
* **Processamento de Dados:** Pandas

## ✨ Funcionalidades

- [x] **Design Responsivo:** Adaptado para dispositivos móveis, tablets e desktop.
- [x] **Tela de Login/Cadastroo:** O sistema permite cadastro, login e logout. As senhas são criptografadas.
- [x] **Lançamentos Financeiros:** O usuário pode registrar entradas (receitas) e saídas (despesas) com valor, data e descrição.
- [x] **Categoria** O usuário pode criar e editar categorias para classificar seus gastos.
- [x] **Gestão de Metas** Uma seção para definir objetivos financeiros com valor alvo e valor já poupado.
- [x] **Dashboard** Visualização gráfica de gastos por categoria, evolução mensal e status das metas.

## 🛠️ Estrutura do Projeto

* `web/`: Container contendo a aplicação Django.
* `db/`: Container do banco de dados PostgreSQL.
* `.env`: Arquivo de variáveis de ambiente (não versionado por segurança).
* `docker-compose.yml`: Configuração dos serviços.

## 📦 Como rodar o projeto

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

### 3. Configuração do 
```bash
# Construir e subir os containers
docker-compose up -d --build

# Executar as migrações do banco de dados
docker-compose exec web python manage.py migrate

# Criar um usuário administrador
docker-compose exec web python manage.py createsuperuser

O sistema estará disponível em: http://localhost:8000 (ou o IP do seu servidor).

## 🔒 Segurança
O arquivo .env deve ser listado no .gitignore para evitar que credenciais sensíveis sejam expostas no repositório. Nunca remova essa proteção.

Desenvolvido por Suzana Cavalcante
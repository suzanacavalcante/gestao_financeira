# 💰 Sistema de Gestão Financeira

> **Status do Projeto:**  🚧 Em desenvolvimento | **Fase Atual do Projeto:** Ajuste da tela de Cadastro e Login, Observabilidade e Testes de Segurança.

## Sobre o Projeto

Este é um projeto de gestão financeira desenvolvido em **Python (Django)**, utilizando **PostgreSQL** como banco de dados e **Docker** para orquestração de ambiente. O projeto inclui dashboards para visualização de gastos e metas.

## Últimas Novidades - 10/02
- **Login e Cadastro**: Novos campos estão sendo adicionados à tela de cadastro.
- **Observabilidade**: Estou adicionando uma ferramenta para monitorar a aplicação. 
- **Testes de Segurança**: Chamei um amigo, Pedro Trugillo para fazer alguns testes de segurança tanto na aplicação quanto em meu servidor.

## Novidades Anteriores
> O PROJETO JÁ POSSUI UMA V1
- **Arquitetura Dockerizada**: Aplicação e Banco de Dados (PostgreSQL) rodando em containers independentes.
- **Deploy em VPS**: Configurado para rodar em ambientes de produção.
- **Segurança**: Logout via POST e proteção de hosts configurada.
- **Estáticos Otimizados**: Uso do WhiteNoise para servir CSS/JS de forma eficiente em produção.

**Link para visualização:** [Acesse aqui o projeto]([PROJETO AINDA EM DESENVOLVIMENTO])

## Tecnologias Utilizadas

### Backend & Web
* **Python 3.11** com **Django 5.2**: Framework principal para lógica de negócio e segurança.
* **Django-auth**: Sistema de autenticação personalizado.
* **WhiteNoise**: Serviço eficiente de arquivos estáticos.

### Infraestrutura & DevOps
* **Docker & Docker Compose**: Containerização de toda a aplicação e banco de dados.
* **Nginx**: Utilizado como Proxy Reverso para gerenciamento de tráfego.
* **Rocky Linux 9.5 (VPS)**: Servidor de hospedagem de nível empresarial.
* **SSL/TLS (HTTPS)**: Implementado via Let's Encrypt para comunicação segura.

### Banco de Dados
* **PostgreSQL**: Banco de dados relacional robusto para garantir a integridade dos dados financeiros.

## Funcionalidades
- [x] Autenticação de usuários (Login/Logout/Cadastro).
- [x] Dashboard dinâmico com resumo financeiro.
- [x] Gestão de Lançamentos (Entradas e Saídas).
- [x] Categorização personalizada.
- [x] Controle de Metas de economia.
- [x] Interface responsiva.

## Estrutura do Projeto

* `web/`: Container contendo a aplicação Django.
* `db/`: Container do banco de dados PostgreSQL.
* `.env`: Arquivo de variáveis de ambiente (não versionado por segurança).
* `docker-compose.yml`: Configuração dos serviços.

## Como rodar o projeto localmente

### 1. Pré-requisitos
Certifique-se de ter instalado em sua máquina ou VPS:
* Docker
* Docker Compose

### 2. Clone o repositório:
```bash
git clone [https://github.com/suzanacavalcante/gestao_financeira.git](https://github.com/suzanacavalcante/gestao_financeira.git)
cd gestao_financeira
```

### 3. Configuração do Ambiente
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
docker-compose exec djangoapp python manage.py createsuperuser
```
O sistema estará disponível em: http://localhost:8000.

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

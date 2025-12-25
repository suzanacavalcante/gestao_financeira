#!/bin/sh

# Encerra a execução do arquivo quando algum comando falhar
set -e

while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
    echo "🟡 Aguardando a Inicialização do Banco de Dados Postgres ($POSTGRES_HOST $POSTGRES_PORT)..."
    sleep 0.1
done

echo "✅ O Banco de Dados Postgres foi Inicializado com Sucesso ($POSTGRES_HOST $POSTGRES_PORT)"

python manage.py collectstatic
python manage.py migrate
python manage.py runserver
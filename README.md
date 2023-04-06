# Sala-de-estudos-virtuais
Projeto de Laboratório de Desenvolvimento de Sistemas 5º Semestre do IFSP

git clone https://github.com/eliascastrosousa/Sala-de-estudos-virtuais

python -m venv env

.\env\scripts\activate

pip install -r requirements.txt

python manage.py makemigrations

python manage.py migrate

python manage.py runserver

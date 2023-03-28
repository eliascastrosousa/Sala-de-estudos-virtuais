## Desenvolvimento Web - Salas-Virtuais
### Tecnologias Utilizadas: Django, Bootstrap, Tailwind.

#### Para executar a aplicação, execute os seguintes comandos:

Instalação do framework Django e Bibliotecas adicionais
~~~powershell
  pip install -r requirements.txt
~~~

Clone para repositório local
~~~powershell
   git clone https://github.com/eliascastrosousa/Sala-de-estudos-virtuais
~~~


Acessar o diretório do projeto<br>
~~~powershell
   cd Sala-de-estudos-virtuais
   cd salas-virtuais
~~~

Executar as migrações do banco de dados
~~~powershell
   python manage.py migrate
~~~

Rodar o servidor
~~~powershell
   python manage.py runserver
~~~

Se caso não tiver os Channels instalado, rodar comando 
~~~powershell
   pip install channels
~~~

Depois rodar o comando runserver

Abra o navegador no endereço http://127.0.0.1:8000/

Para executar testes automatizados
~~~powershell
   python manage.py test salas_virtuais
~~~



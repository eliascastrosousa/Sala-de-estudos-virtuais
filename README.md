## Sala de estudos virtuais
Projeto de Laboratório de Desenvolvimento de Sistemas 5º Semestre do IFSP

### Requisitos

Sala de estudos virtuais

O estudo, em grupo, pode ser motivador uma vez que o apoio de colegas pode auxiliá-lo com temas desafiadores.

Neste sentido, é interessante que estudantes possam se encontrar em uma sala de estudos comum e se preparar para qualquer tipo de tema junto com outros alunos que estão estudando para o mesmo assunto. Um sistema de salas virtuais de estudos, portanto, faz sentido nesse contexto.

O sistema de sala de estudos virtuais deverá permitir que os alunos se conectem por meio de um chat de texto, o qual deverá ter seu histórico arquivado diariamente e disponibilizado para acesso dos estudantes em datas futuras. Os alunos também deverão ser capazes de compartilhar material de estudo em distintos formatos (.pdf , .doc e .docx, .xls e .xlsx, além de .zip). O sistema também deverá permitir que professores elaborem guias de estudo, além de inserirem material complementar e poder ministrar sessões de dúvidas com os alunos.

---

Para o chat funcionar, é necessário instalar o VS Microsoft C++ Build Tools:

https://github.com/bycloudai/InstallVSBuildToolsWindows

~~~powershell
  git clone https://github.com/eliascastrosousa/Sala-de-estudos-virtuais
~~~

~~~powershell
  python -m venv env
~~~

~~~powershell
  .\env\scripts\activate.ps1
~~~

~~~powershell
  pip install -r requirements.txt
~~~

~~~powershell
  python manage.py makemigrations
~~~

~~~powershell
  python manage.py migrate
~~~

~~~powershell
  python manage.py runserver
~~~







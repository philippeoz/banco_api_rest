API RESTful - Banco de Tangamandápio ^^
====

Recentemente, o Banco de Tangamandápio resolveu trocar os sistemas de seus caixas eletrônicos
por uma interface web e eu fui responsável por escrever uma parte do backend. O novo sistema
 se conecta a uma API RESTful para obter as informações, enquanto toda a parte visual
roda em um navegador no "caixa eletrônico".
O backend foi escrito em Python e disponibiliza alguns endpoints para que o caixa
eletrônico consiga se conectar. A lista deles é:

    * GET /conta/

    * POST /conta/

    * GET /conta/{id}/

    * POST /conta/{id}/saque/

    * POST /conta/{id}/transferencia/

    * POST /conta/{id}/extrato/

    * GET /caixa/

    * POST /caixa/

---
Como executar?
---
1. Criar e ativar um [ambiente virtual](http://docs.python-guide.org/en/latest/dev/virtualenvs/)
    * `mkvirtualenv banco_tangamandapio` para criar um virtualenv chamado banco_tangamandapio
    * `workon banco_tangamandapio` para ativar o virtualenv sempre que for trabalhar no projeto

2. Instalar as dependências
    * `pip install -r requirements.txt`

3. Depois de instaladas as dependências, basta executar o comando:
    * `python manage.py runserver`
    * O sistema criará o banco de dados caso não exista.
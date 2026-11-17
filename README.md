# Instituto Refúgio Literário

Sistema web para apoiar o gerenciamento do acervo de uma biblioteca comunitária, substituindo controles manuais em cadernos e planilhas.

## Funcionalidades do MVP

- Cadastro e consulta de livros.
- Cadastro e consulta de participantes.
- Registro de empréstimos e devoluções.
- Indicação de exemplares disponíveis e empréstimos atrasados.
- Testes automatizados com pytest.
- Integração contínua com GitHub Actions.

## Tecnologias

Python 3.12, Flask 3, Flask-SQLAlchemy (SQLAlchemy 2), SQLite, Jinja2, Bootstrap 5.3 e pytest.

## Requisitos

- Python 3.12 instalado.
- Git instalado.

## Como executar localmente

1. Clone o repositório e entre na pasta do projeto.
2. Crie um ambiente virtual:

   ```bash
   python -m venv .venv
   ```

3. Ative o ambiente virtual:

   Windows PowerShell:
   ```powershell
   .venv\Scripts\Activate.ps1
   ```

   Linux/macOS:
   ```bash
   source .venv/bin/activate
   ```

4. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

5. Defina uma chave secreta para o ambiente:

   Windows PowerShell:
   ```powershell
   $env:SECRET_KEY="uma-chave-local-segura"
   ```

   Linux/macOS:
   ```bash
   export SECRET_KEY="uma-chave-local-segura"
   ```

6. Inicie a aplicação:

   ```bash
   python run.py
   ```

7. Acesse http://127.0.0.1:5000.

O banco SQLite é criado automaticamente na pasta `instance` na primeira execução.

## Executar os testes

```bash
pytest -q
```

## Observações sobre o MVP

O sistema coleta somente os dados básicos necessários à operação. Para uso real, devem ser definidos procedimentos de backup, controle de acesso por usuário, política de privacidade, gestão de credenciais e revisão de segurança. A chave secreta de produção deve ser configurada por variável de ambiente.

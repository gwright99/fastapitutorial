# fastapitutorial

TODO: Add stuff later.

!!! warning "Important Distinction!"

    [https://fastapi.tiangolo.com/tutorial/body/#use-the-model](https://fastapi.tiangolo.com/tutorial/body/#use-the-model):

    - If the parameter is also declared in the path, it will be used as a path parameter.
    - If the parameter is of a singular type (like int, float, str, bool, etc) it will be interpreted as a query parameter.
    - If the parameter is declared to be of the type of a Pydantic model, it will be interpreted as a request body.

    I declared an endpoint with 4 individual parameters: 1 came from path, the other 3 were in function declaration. Sending body via `requests` did not work, which I now see is due to my failure to use Pydantic model to define.

!!! warning "?TestClient / PyTest? Still expects `default` on Path"

    New versions of [FastAPI don't require it](https://stackoverflow.com/questions/77154013/fastapi-path-typeerror-path-missing-1-required-positional-argument-defaul) but it looks like TestClient/PyTest still do:

    ```python
    ImportError while loading conftest '~/fastapitutorial/tests/conftest.py'.
    tests/conftest.py:4: in <module>
        from app.app import app
    src/app/app.py:133: in <module>
        item_id: int = Path(ge=0),
    E   TypeError: Path() missing 1 required positional argument: 'default'
    ```

    Fix with `default=...`:

    ```python
    item_id: int = Path(default=..., ge=0)
    ```


## Setup

### PYTHONPATH
```bash
# To avoid relative imports
$  export PYTHONPATH=~/fastapitutorial/src/app
```

### VSCODE / Pylance
Add extra config in `<PROJ_ROOT>/.vscode/settings.json`

```yaml
{
    "python.testing.pytestArgs": [
        "."
    ],
    "python.testing.unittestEnabled": false,
    "python.testing.pytestEnabled": true,

    "python.analysis.extraPaths": [
        "~/fastapitutorial/src/app"
    ],

    "python.autoComplete.extraPaths": [
        "~/fastapitutorial/src/app"
    ]
}
```

## Testing
See PKB (Python/Setup) for explanation re: `src` folder and how packages are locally installed (`pip3 install -e .`). Means one can now avoid the headaches of messing with `sys.path` in order for the separate peer `/tests` folder to get access to application code.

```bash
cd <ROOT>
mypy src
flake8 src
pytest
```


## Pushing Image
```bash
docker build -t ghcr.io/gwright99/fastapitutorial:latest .
docker push ghcr.io/gwright99/fastapitutorial:latest
```

## Run locally so I can test with `requests`
```bash
$ fastapi run src/app/app.py --port 8080 --reload
# Change port to not conflict with postgres adminer:
$ $ fastapi run src/app/app.py --port 5000 --reload
$ pytest -vs   # Note that I changed ENDPOINT in test file.
```

## Testing Errors
`HTTP 503` error result either from the Pod being broken or the HTTPRoute not having been updated.

`TypeError: unsupported operand type(s) for |: 'type' and 'type'` <-- occurred when running app in container (used Python3.10 locally, container was based on Python3.9, `|` type operator introduced in Python3.10). [Source](https://github.com/fastapi/typer/issues/371)


## SQLAlchemy
Benefit: provide common way to interface regardless of underlying DB. 

## TODO:
- Pull secrets from something more secure than local .env
- SqlAlchemy:
    - relationship; back_populates
    - index=True
    - why does `from db.base import Base` pull in the children based on `Base`?
- Alembic
    - Why does Alembic need me to import derived classes into `db.base` and then work when `alembic/env.py` simply imports the Base class??

## Postgres commands
```bash
$ sudo -u postgres psql

# Cannect to adminer for visual 
> \l  # means show all databases
> \c dbname : to connect to a database
> \dt : to see tables in the database

> CREATE DATABASE blogdb;
> CREATE USER nofoobar WITH ENCRYPTED PASSWORD 'supersecret';
> GRANT ALL PRIVILEGES ON DATABASE blogdb TO nofoobar
```

## Alembic
```bash
$ alembic init alembic
$ alembic revision --autogenerate -m "first commit"   # < creates empyt upgrade / downgrade

$ alembic revision --autogenerate -m "create user and blog table migrations"  #analyzes tables and creates a migration file
$ alembic upgrade head   #executes the migration files to make actual changes in db
$ alembic downgrade -1   # Go back one step. DESTRUCTIVE.
$ alembic downgrade <HASH>
$ alembic downgrade base  # very start

$ alembic history
  <base> -> c095296de2bf (head), create user and blog table migrations
```

See DB connection either (1) hardcoded in `alembic.ini` (bad), or via `alembic/env.py` (import dotenv value).
Based on postion of `.ini` file (`/src/app/alembic.ini`), I have to move the `.env` back into the `/src/app`) folder. This means the `fastapi run ...` command needs to fix its path.

First migration created file in `src/app/alembic/versions/ALPHANUMERIC_first_commit.py`.


## Pylance Errors
```python
# type: ignore      <-- inline, suppress Pylance error
```

## Queries to PostGres via SQLAlchemy
```python
>>> from db.models.user import User
>>> from db.session import get_db
Database URL is  postgresql://nofoobar:supersecret@localhost:5432/blogdb
>>> db = get_db().__next__()
>>> db.query(User).all()
[]
```


## Passlib
Static Method -- do not need an instance to be created before calling. Can be called directly against import.

Error in logs (but does not break, related to latest `bcrypt`):
```python
>>> Hasher.get_password_hash("supersecret1234")
(trapped) error reading bcrypt version
Traceback (most recent call last):
  File "/home/deeplearning/fastapitutorial/venv/lib/python3.10/site-packages/passlib/handlers/bcrypt.py", line 620, in _load_backend_mixin
    version = _bcrypt.__about__.__version__
AttributeError: module 'bcrypt' has no attribute '__about__'
'$2b$12$2nBbe/fhuYjoxujpLYAQ.uFgxRheihMWPXKPgve0ycGB.BJVuWe/G'
```

Solveable by logging config or dataclass patch: https://github.com/pyca/bcrypt/issues/684


# Badge
![Unit Tests](https://github.com/gwright99/fastapitutorial/actions/workflows/unittest.yaml/badge.svg)
![PR Test](https://github.com/gwright99/fastapitutorial/actions/workflows/pr_test.yaml/badge.svg)

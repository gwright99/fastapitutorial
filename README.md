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
Add extra config in `<PROJ_ROOT>/.vscode/settings.json`:

- pytest args
- analysis / code completion paths
- flake8 codes to ignore


## Testing
See PKB (Python/Setup) for explanation re: `src` folder and how packages are locally installed (`pip3 install -e .`). Means one can now avoid the headaches of messing with `sys.path` in order for the separate peer `/tests` folder to get access to application code.

```bash
cd <ROOT>
mypy src
flake8 src
pytest
```

Changing source code folder from `app` to `src` meant that i broke the `coverage` configuration in `pyproject.toml`. Had to change `--cov=app` to `--cov=src`. Then invoke the tests from `~/fastapitutorial`.


## Pushing Image
```bash
docker build -t ghcr.io/gwright99/fastapitutorial:latest .
docker push ghcr.io/gwright99/fastapitutorial:latest
```

## Run locally so I can test with `requests`
```bash
$ fastapi run src/app/app.py --port 8080 --reload
# Change port to not conflict with postgres adminer:
# $ $ fastapi run src/app/app.py --port 5000 --reload
$ cd ~/fastapitutorial/src && fastapi run app/app.py --port 5000 --reload    # gets .env values
$ pytest -vs   # Note that I changed ENDPOINT in test file.
```

## Testing Errors
`HTTP 503` error result either from the Pod being broken or the HTTPRoute not having been updated.

`TypeError: unsupported operand type(s) for |: 'type' and 'type'` <-- occurred when running app in container (used Python3.10 locally, container was based on Python3.9, `|` type operator introduced in Python3.10). [Source](https://github.com/fastapi/typer/issues/371)


## SQLAlchemy
Benefit: provide common way to interface regardless of underlying DB.


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


## Design Patterns
- "Repository Pattern" -- separate **route** logic from **database interaction (i.e. ORM)** code. Essentially, the route logic calls a separate function which will use the ORM to interact with the DB.


# Pre-Commit Checks
`.pre-commit-config.yaml`

Full list of hooks: [https://github.com/pre-commit/pre-commit-hooks](https://github.com/pre-commit/pre-commit-hooks)

Problems installing. `$ pre-commit install` throws error (since I have hooks in `.githooks`):
```bash
$ pre-commit install
    [ERROR] Cowardly refusing to install hooks with `core.hooksPath` set.
    hint: `git config --unset-all core.hooksPath`
```

Solved with:
```bash
# https://stackoverflow.com/questions/67793193/cowardly-refusing-to-install-hooks-with-core-hookspath-set
$ GIT_CONFIG=/dev/null pre-commit install
```

Note: Only runs on **staged files**.

Put `pre-commit` command at top of `.githooks/pre-commit` -- might be ok solution? Added extra Bash logic to make sure local versions are stepped on by global.

If changes are made by pre-commit steps. commit fails -- you must look at the changes and re-add & re-commit. Feels convoluted but asotille says this is done on purpose for a human to be in the mix. See [Add changes generated by pre-commit
#879](https://github.com/pre-commit/pre-commit/issues/879)  for some more advanced Git commmands which can be used to limit scope of changed files (`git apply --reverse ...` was quite scary!).

Seems easier to use VSCode plugins that do some of this automatically for me at save time. Alternatively, use `pre-commit run` PRIOR to `git commit` to see error that would have been surfaced/fixed by `git commit` (_downside is that you still need to add the files first_).

To avoid pre-commit hooks, use:: `git commit -m "my message" --no-verify`.
To run pre-commit hooks on the entire codebase, use: `pre-commit run --all-files`.


## Multiple Config for same thing:
Figure out how best to organize all this both locally and when it gets [pushed to CICD](https://pre-commit.com/#usage-in-continuous-integration). Example:

- Flake8
    - `.vscode/settings.json` has `flake` plugin settings.
    - `setup.cfg` had `[flake8] section
    - `.pre-commit-config.cfg` has flake8 args


## TODO:
- Pull secrets from something more secure than local .env
- General:
    - Since `alembic upgrade head` creates tables in the DB, why do I need to run a creation function in app.py?
      NOTE: Doesn't seem like I need to -- the alembic upgrade creates the tables and subsequent calls for DB
      transactions work. Tutorial badly explained here. [https://fastapitutorial.com/blog/creating-tables-in-fastapi/](https://fastapitutorial.com/blog/creating-tables-in-fastapi/)
      HOWEVER,
- SqlAlchemy:
    - relationship; back_populates
    - index=True
    - why does `from db.base import Base` pull in the children based on `Base`?
- Alembic
    - Why does Alembic need me to import derived classes into `db.base` and then work when `alembic/env.py` simply imports the Base class??
- FastAPI:
    - Depends
    - Dependency Injection / monkey-patching `get_db`?
    - Why am I importing `sqlalchemy.orm > Session` when we did SessionLocal earlier? Oh, it's like an Interface?
    - `orm_mode = true` works how?
    - `async def` functions vs synchronous functions (eg. `create_user` synchronous but `create_blog` async)


## Alembic Migrations
Running the alembic migrations will not only apply changes to the database, but also create the tables and columns in the first place. This is why you don’t find any table creation command like `Base.metadata.create_all(bind=engine)` which you’ll often find in tutorials that don’t cover migrations.

RUN everything from `src/`  <-- DOES THIS BREAK TESTING?


Change how Alembic names migrations (e.g. `YYYYMMDDHHMMSS`): https://medium.com/alan/making-alembic-migrations-more-team-friendly-e92997f60eb2 (in `migrations/env.py` )

```bash
# Run table migration
$ cd ~/fastapitutorial/src
$ ./scripts/boot_prestart.sh
```

## SQLAlchemy
I rewrote the `model` entries based on SQLAlchemy guidance here: [ORM Declarative Models](https://docs.sqlalchemy.org/en/20/changelog/whatsnew_20.html#orm-declarative-models). Items of note:

- `Column` replaced with `mapped_column`
- `Mapped[<type>]` can now live on left size.
    - `Optional[<type>]` on left now means you don't need to declare `nullable=True` on right (absence of `Optional` will cause SQLAlchemy to set `nullable=False`).


## Flake8
Moved config to `.flake8` file (_commented out most config in `.vscode/settings` except to point to `.flake8`). Commented out setup.cfg too (_must close VSCODE and reopen for this to work!_)
https://stackoverflow.com/questions/74400353/vscode-flake8-ignore


## `crud/` folder
Super important for scaling. Revisit the logic.

## `requests` vs `httpx`
Can requests do async ye (httpx can).


# Rename
Changed `app.py` to `main.py` since it seemed to be conflicting with the overarching `app` folder.

```
# From `./scripts/boot_prestart.sh`
/home/deeplearning/fastapitutorial/src
Traceback (most recent call last):
  File "/home/deeplearning/fastapitutorial/src/app/boot_02_load_initial_data.py", line 9, in <module>
    from app import crud, models, schemas  # noqa: F401
  File "/home/deeplearning/fastapitutorial/src/app/app.py", line 9, in <module>
    from app.api.api_v1.router import api_router as v1_router
ModuleNotFoundError: No module named 'app.api'; 'app' is not a package
```

## FASTAPI Trick
```python
@router.post("/token", response_model=Token)
def login( db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends() ) -> Any:
```

Note how `db` must explicitly define `get_db` as its dependency.
Note how `form_data` does not explicitly define its dependency. 

Why?
> Depends() without arguments is just a [shortcut](https://fastapi.tiangolo.com/tutorial/dependencies/classes-as-dependencies/?h=%20class%20depe#shortcut) for [classes as dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/classes-as-dependencies/). [SOURCE](https://stackoverflow.com/questions/65059811/what-does-depends-with-no-parameter-do)

aka `commons: CommonQueryParams = Depends(CommonQueryParams)` == `commons: CommonQueryParams = Depends()`.

> When you use a Pydantic Model with Depends, it makes the Pydantic fields query-type parameters on the API endpoint. [SOURCE](https://stackoverflow.com/questions/65059811/what-does-depends-with-no-parameter-do)



# This will try to extract the 'Authorization: Bearer xxx' value from a request to the endpoint and then pass
# the value to the `/token` endpoint for extraction. If Bearer not present, returns 401.
# https://stackoverflow.com/questions/67307159/what-is-the-actual-use-of-oauth2passwordbearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


### JWT
Using scopes for authorization
Refresh tokens
Password resets
Single Sign On (SSO)
Adding custom data to the JWT payload
JSON Web Encryption


## Deprecation Warning (multipart vs python_multipart)
```bash
venv/lib/python3.10/site-packages/fastapi/dependencies/utils.py:94
  /home/deeplearning/fastapitutorial/venv/lib/python3.10/site-packages/fastapi/dependencies/utils.py:94: PendingDeprecationWarning: Please use `import python_multipart` instead.
    from multipart import __version__
```

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html

- `nano venv/lib/python3.10/site-packages/starlette/formparsers.py`
- nano venv/lib/python3.10/site-packages/starlette/requests.py`

```python
#    from multipart.multipart import parse_options_header
    from python_multipart.multipart import parse_options_header
```

Fix:
Manually patched all the following lines: `multipart` -> `python_multipart`

```bash
venv/lib/python3.10/site-packages/starlette/requests.py:16:    from multipart.multipart import parse_options_header
venv/lib/python3.10/site-packages/starlette/formparsers.py:13:    from multipart.multipart import parse_options_header
venv/lib/python3.10/site-packages/starlette/formparsers.py:19:    from multipart.multipart import MultipartCallbacks, QuerystringCallbacks
venv/lib/python3.10/site-packages/fastapi/dependencies/utils.py:94:        from multipart import __version__
venv/lib/python3.10/site-packages/fastapi/dependencies/utils.py:99:            from multipart.multipart import parse_options_header

(venv) deeplearning@DESKTOP-1ST9352:~/fastapitutorial$ grep --recursive --line-number 'import multipart' venv/
venv/lib/python3.10/site-packages/starlette/formparsers.py:12:    import multipart
```
NOTE: This fixed the Pydantic deprecation warning in pytest but then subsequently broke FastAPI's OAuth2PasswordRequestFrom capabilities. So I reverted all changes. ["There was an error parsing the body"](https://github.com/fastapi/fastapi/issues/1604)

## Testing
```bash
cd ~/fastapittutorial/ && pytest -vs tests/test_recipe.py
```

Using `mocking` library MagicMock and FastAPI dependency replacement to test endpoints. Replacement method is interesting but definitely is more to the "totally mocked out".


# Gunicorn vs Uvicorn
Traditional suggestion when deploying FastAPI app to prod is run **both** Uvicorn and Gunicorn (_referred to a `Guvicorn` _) to get best of concurrency parallelism:

1. Tell Uvicorn to run multiple worker processes (Gunicorn-compatible Uvicorn worker class).
2. Include Gunicorn as a management tool for:
    
    - Managing dead processses / restarting stuck processes
    - Take advantage of multi-core CPUs

aka:
```bash
# Local dev
$ uvicorn --reload

# Prod
$ gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:80
```

For deploying to Kubernetes, however, [FastAPI docs](https://fastapi.tiangolo.com/bn/deployment/docker/#replication-number-of-processes) suggest a **single process per pod**. [Reddit thread](https://www.reddit.com/r/FastAPI/comments/1dkpu11/does_uvicorn_handle_multiple_requests_at_once/) says K8s is doing same thing as Gunicorn -- health checks and recycling dead pods. Better to have single processes sipping a single CPU and min RAM rather than fatter pod with requires more resources (e.g. 1 CPU / 150 MB RAM per Pod vs 4 CPU and 600 MB RAM per Pod).


## Testing -- Setting environment variables easily
- https://pytest-with-eric.com/pytest-best-practices/pytest-environment-variables/

Using `pytest-env` and `pytest.ini` in `tests` folder.
NOTE: FOUR (x4) slashes needed for `sqlite` URLs! 

Nov 9/2024 - rewrote components to allow same project structure / setup to work for both live FASTAPI deployment and emulated TestClient-based testing. 

1. Expectation is that all commands are launched from the PROEJCT ROOT (_i.e. `~/fastapitutorial`).
2. `alembic.ini > script_location` changed to `src/migrations`.
3. `boot_prestart.sh` changed so that paths are all relative to PROJECT ROOT.
4. `pytest.ini` added to `tests/` to set an environment variable indicating a testing run was active.
5. `src/core/config.py` updated to include `TEST_DB_FILE` and `TEST_DB_URL` to centralize testing db config with prod db config.
6. `src/db/session.py` updated to dynamically populate engine with appropriate config based on present of testing flag / db prefix of `SQLALCHEMY_DATABASE_URL
7. `src/migrations/env.py` modified with if statement looking for `FASTAPI_TESTING_RUN_ACTIVE` envvar. If yes, different DB connection string used for migration.
6. `conftest.py` added to `tests/test_with_testclient`. 
    - Activated `pytest_sessionstart` function to prep local SQLITE testing db.
    - Activated `pytest_sessionfinish` to delete test db from local file system.
conftest destroy db


Testing GHA via ACT: 

1. Execute with: `~/fastapitutorial$ gh act -j test -W .github/workflows/unittest.yaml`
2. To emulate local upload had to add extra config to `~/.config/act/actrc`  (pointing to /tmp/.act). See: [https://github.com/nektos/act/issues/1929](https://github.com/nektos/act/issues/1929)
3. Split testing into two sections:
    - Emulation with TestClient
    - Running actual instance of FastAPI server with localhost calls via requests.
4. Updated `act` command to accommodate need for .env file for fastapi instanc (from `~/fastapitutorial`): `gh act -j test -W .github/workflows/unittest.yaml -s ENVFILE=$(base64 .env -w 0)` 
    - Had to creae secret ENVFILE in GH repo as well (populated with base64-encoded .env file).


## Secrets
Need to find a consistent way to harmonize files in local `.env`, with GHA Secret, with K8s pod. Currently

1. GHA Secret created via cut-and-paste of B64ed local .env.
2. K8s pod populated by hardcoded init container.

Idea: Helper script. Can use GH CLI to harmonize GH. Need to figure out how to push SSH commands through to local basstion server to be able to populate via local cluster's `kubectl`. Alternatively, use Vault instance as core distribution mechanism.

SOLUTION:
`~/fastapitutorial/src/scripts/harmonize_secrets.sh`. Does two things:

1. Creates `ENVFILE` Secret in GH repo (_accessible to `gwright99/fastapitutorial`).
2. Creates K8s Secret `envfile` in namespace `fastapi`. Deployment manifest has init container to copy and decode the content into the cloned repo in the expected location.

# Badge
![Unit Tests](https://github.com/gwright99/fastapitutorial/actions/workflows/unittest.yaml/badge.svg)
![PR Test](https://github.com/gwright99/fastapitutorial/actions/workflows/pr_test.yaml/badge.svg)

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)

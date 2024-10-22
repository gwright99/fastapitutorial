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
$ fastapi run src/app/app.py --port 8080
$ pytest -vs   # Note that I changed ENDPOINT in test file.
```

## Testing Errors
`HTTP 503` error result either from the Pod being broken or the HTTPRoute not having been updated.

# Badge
![Unit Tests](https://github.com/gwright99/fastapitutorial/actions/workflows/unittest.yaml/badge.svg)
![PR Test](https://github.com/gwright99/fastapitutorial/actions/workflows/pr_test.yaml/badge.svg)

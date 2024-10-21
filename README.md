# fastapitutorial

TODO: Add stuff later.

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

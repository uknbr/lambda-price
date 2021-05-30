# lambda-price
AWS lambda to check prices

## Build & Test

```bash
make package
make run
```

## Usage
- Deploy

```bash
serverless deploy
```

- Invoke 

```bash
serverless invoke -f main -p data.json -l
```

- Remove

```bash
serverless remove
```

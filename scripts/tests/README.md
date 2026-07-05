# 🧪 Tests

Unit tests untuk scripts di folder ini. Run dengan:

```bash
cd scripts
PYTHONPATH=. pytest tests/
```

## Coverage

| Script | Test Coverage |
|---|---|
| `check_token.py` | Mint/freeze auth detection, holders %, score calc |
| `wallet_setup.py` | Encryption round-trip, key derivation |
| `rug_score.py` | All scoring branches |
| `lp_check.py` | Filter logic |

## Note

Tests menggunakan **mocked HTTP responses** agar tidak butuh API key saat testing.

```bash
# Run with verbose
pytest tests/ -v

# Run specific test
pytest tests/test_rug_score.py -v

# Coverage report
pytest tests/ --cov=. --cov-report=term-missing
```

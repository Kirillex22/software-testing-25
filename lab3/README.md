# main terminal (все выполняется из папки lab3)

```bash
    sudo apt update
    sudo apt install snapd -y
    sudo snap install k6
    k6 version
```

```bash
    python3 -m venv .venv
    source .venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
```

```bash
    python3 app.py
```

# locust terminal

```bash
    source .venv/bin/activate
    locust -f locustfile.py --host=http://127.0.0.1:5000
```

# k6 terminal

```bash
    k6 run load_tests/stress_test.js
```

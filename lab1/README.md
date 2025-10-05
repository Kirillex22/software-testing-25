# Лабораторная работа "Behavior-Driven Development"

## Как запустить проект?

### Требования
- Установленный Python 3.12
- Установленный Git

### Шаги по установке
1) Клонируйте репозиторий
```bash
    git clone https://github.com/Kirillex22/software-testing-25.git
    cd software-testing-25
```
2) Перейдите на нужную ветку
```bash
    git checkout feature-lab-bdd
    cd lab1
```
3) Создайте и активируйте виртуальное окружение, а также установите необходимые зависимости
```bash
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
```
4) Установите pre-commit hook
```bash
    pre-commit install       # установит хуки в локальный .git/hooks
```
5) Запустите тесты
```bash
    behave features
```

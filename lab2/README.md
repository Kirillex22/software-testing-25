# Лабораторная работа "Интеграционное тестирование"

Для работы необходим `Docker` (контейнеры для `Postgres + Kafka`), а также `Python 3.12`.

## Установка Docker

```bash
    sudo apt update
    sudo apt upgrade -y
    sudo apt install -y ca-certificates curl gnupg lsb-release
    sudo mkdir -p /etc/apt/keyrings
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
    echo \
    "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
    $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    sudo apt update
    sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
    docker --version
    docker compose version
    sudo usermod -aG docker $USER
    newgrp docker
```

## Запуск проекта

1) Клонируйте репозиторий и перейдите в папку `lab2`
```bash
    git clone https://github.com/Kirillex22/software-testing-25.git
    git checkout feature-integration-testing
    cd software-testing-25/lab2
```
2) Создайте `.env` файл по образцу из `.env.example` (можно просто переименовать)
3) Создайте виртуальное окружение и активируйте его
```bash
     python3 -m venv .venv
     source .venv/bin/activate
```
4) Установите зависимости 
```bash
    pip install -r requirements.txt
```
5) Запустите тесты 
```bash
    pytest
```

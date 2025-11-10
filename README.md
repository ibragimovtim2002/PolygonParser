# Polygon Parser

**Polygon Parser** — это Django-приложение для работы с токенами в сети Polygon.  
Позволяет получать балансы адресов, топ-холдеров, историю транзакций и информацию о токенах через встроенные API.  

---
## Технологии:
- Python 3.11
- Django
- Django REST Framework
- Web3.py — для взаимодействия с сетью Polygon
- The Graph Token API — для получения холдеров и транзакций
- PolygonScan API (опционально)
---

## Установка и запуск

1. Клонировать репозиторий:
  ```text
git clone https://github.com/ibragimovtim2002/PolygonParser.git
  ```
2. Создать и активировать виртуальное окружение:
```text
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows
```
4. Установить зависимости:
```text
pip install -r requirements.txt
   ```
5. Настраиваем config.py:
```text
POLYGON_RPC = "https://polygon-rpc.com"
TOKEN_ADDRESS = "0x1a9b54a3075119f1546c52ca0940551a6ce5d2d0"
THE_GRAPH_JWT = "<YOUR_THEGRAPH_API_KEY>"
POLYGONSCAN_API_KEY = "<YOUR_POLYGONSCAN_API_KEY>"
```
6. Запустить сервер
```text
python manage.py runserver
```
Сайт будет доступен по адресу: http://127.0.0.1:8000/
---

## Уровни функциональности

### **Уровень A** — Получить баланс выбранного адреса

Пример запроса:
```text
GET /api/balance/0x51f1774249Fc2B0C2603542Ac6184Ae1d048351d/
```

### **Уровень B** — Получить баланс нескольких адресов сразу

Пример запроса:
```text
POST /api/balances/
Content-Type: application/json
{
  "addresses": [
    "0x51f1774249Fc2B0C2603542Ac6184Ae1d048351d",
    "0x4830AF4aB9cd9E381602aE50f71AE481a7727f7C"
  ]
}
```

### **Уровень C** — Получить топ N адресов по балансам токена

Пример запроса:
```text
GET /api/top/5/
```

### **Уровень D** — Получить топ N адресов с датами последних транзакций

Пример запроса:
```text
GET /api/top_with_tx/3/
```

### **Уровень E** — Произвольная работа по любому из токенов

Пример запроса информации о токене:
```text
GET /api/getinfo/token/<token_address>/
```
Пример запроса информации топ-ходеров введенного токена:**
```text
GET /api/getinfo/holders/<token_address>/<top_n>/
```

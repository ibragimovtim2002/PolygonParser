import requests
from config import TOKEN_ADDRESS, POLYGONSCAN_API_KEY, THE_GRAPH_TOKEN_API_URL, THE_GRAPH_JWT, NETWORK

def get_top_holders(top_n: int) -> list[tuple[str, float]]:
    """
    Получает топ N адресов по балансу токена через PolygonScan API.
    Возвращает список кортежей: [(address, balance), ...]
    Нужен платный доступ к PolygonScan API.
    """
    url = "https://api.polygonscan.com/api"
    params = {
        "module": "token",
        "action": "topholders",
        "contractaddress": TOKEN_ADDRESS,
        "offset": top_n,
        "apikey": POLYGONSCAN_API_KEY,
        "chainid": 137
    }

    response = requests.get(url, params=params)
    data = response.json()

    if data["status"] != "1":
        raise ValueError(f"Ошибка PolygonScan API: {data.get('result')}")

    holders = []
    for item in data["result"]:
        address = item["HolderAddress"]
        balance = int(item["Balance"]) / 10**18
        holders.append((address, balance))

    return holders

def get_top_holders_thegraph(top_n: int) -> list[tuple[str, float]]:
    """
    Получает топ N держателей токена через The Graph API.

    Args:
        top_n (int): количество топ-адресов для получения.

    Returns:
        list[tuple[str, float]]: список кортежей (address, balance),
        где `address` — адрес держателя, а `balance` — баланс токена.

    Raises:
        requests.RequestException: если запрос к API не удался.
        ValueError: если данные API имеют неожиданный формат.

    Notes:
        - Использует THE_GRAPH_TOKEN_API_URL, NETWORK, TOKEN_ADDRESS и THE_GRAPH_JWT.
        - Предполагается, что API возвращает JSON с ключом "data", содержащим список держателей.
    """
    url = f"{THE_GRAPH_TOKEN_API_URL}/v1/evm/holders"
    params = {
        "network": NETWORK,
        "contract": TOKEN_ADDRESS,
        "limit": top_n,
        "page": 1
    }
    headers = {"Authorization": f"Bearer {THE_GRAPH_JWT}"}

    resp = requests.get(url, headers=headers, params=params)
    data = resp.json()

    # предполагаем что в data есть список держателей с адресами и балансами
    holders = []
    for item in data.get("data", []):
        address = item["address"]
        balance = float(item["value"])
        holders.append((address, balance))
    return holders

def get_top_with_last_transactions_thegraph(top_n: int) -> list[tuple[str, float, str]]:
    """
    Получает топ N держателей токена через The Graph API вместе с датой последней транзакции.

    Args:
        top_n (int): количество топ-адресов для получения.

    Returns:
        list[tuple[str, float, str]]: список кортежей (address, balance, last_tx_date),
        где:
            - address (str) — адрес держателя,
            - balance (float) — баланс токена,
            - last_tx_date (str) — дата последней транзакции (может быть None).

    Raises:
        requests.RequestException: если запрос к API не удался.
        ValueError: если данные API имеют неожиданный формат.

    Notes:
        - Использует THE_GRAPH_TOKEN_API_URL, NETWORK, TOKEN_ADDRESS и THE_GRAPH_JWT.
        - Предполагается, что API возвращает JSON с ключом "data", содержащим список держателей.
        - Дата последней транзакции извлекается из поля "last_update" API.
    """

    url = f"{THE_GRAPH_TOKEN_API_URL}/v1/evm/holders"
    headers = {"Authorization": f"Bearer {THE_GRAPH_JWT}"}
    params = {
        "network": NETWORK,
        "contract": TOKEN_ADDRESS,
        "limit": top_n,
        "page": 1
    }

    resp = requests.get(url, headers=headers, params=params)
    data = resp.json()

    holders = []
    for item in data.get("data", []):
        address = item["address"]
        balance = float(item["value"])
        last_tx_date = item.get("last_update")
        holders.append((address, balance, last_tx_date))

    return holders
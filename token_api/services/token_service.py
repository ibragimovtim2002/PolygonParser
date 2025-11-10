import requests
from web3 import Web3
from config import TOKEN_ADDRESS, POLYGONSCAN_API_KEY, THE_GRAPH_TOKEN_API_URL, THE_GRAPH_JWT, NETWORK
from .web3_client import w3
from multicall import Call, Multicall

ERC20_ABI = [
    {
        "constant": True,
        "inputs": [{"name": "_owner", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"name": "balance", "type": "uint256"}],
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "decimals",
        "outputs": [{"name": "", "type": "uint8"}],
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "symbol",
        "outputs": [{"name": "", "type": "string"}],
        "type": "function",
    },
]

contract = w3.eth.contract(address=TOKEN_ADDRESS, abi=ERC20_ABI)

def get_balance(address: str) -> dict:
    """Возвращает баланс токена для указанного адреса"""
    addr = Web3.to_checksum_address(address)
    balance = contract.functions.balanceOf(addr).call()
    decimals = contract.functions.decimals().call()
    symbol = contract.functions.symbol().call()
    return {
        "address": address,
        "balance": balance / 10**decimals,
        "symbol": symbol,
    }

def get_balances_batch(addresses: list[str]) -> list[float]:
    """Возвращает список балансов токена для нескольких адресов"""
    balances = []
    for addr in addresses:
        try:
            balances.append(get_balance(addr)["balance"])
        except Exception:
            balances.append(None)  # если адрес некорректный
    return balances

def get_balances_batch_update(addresses: list[str]) -> list[float]:
    """
    Оптимальный batch-вызов для нескольких адресов через Multicall.
    Возвращает список балансов токена.
    Не работает, выдается ошибка:
        Cannot connect to host polygon-rpc.com:443 ssl:True
        [SSLCertVerificationError: (1, '[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed:
        unable to get local issuer certificate (_ssl.c:992)')] [0]
    Доработка функции уменьшит количество обращений к RPC: вместо кошелек-запрос будет
    все кошельки-запрос, требуется доработать, пока действует старая версия
    """
    decimals = contract.functions.decimals().call()
    calls = []
    for addr in addresses:
        addr = Web3.to_checksum_address(addr)
        calls.append(Call(TOKEN_ADDRESS, ['balanceOf(address)(uint256)', addr], [[addr, None]]))

    multi = Multicall(calls=calls, _w3=w3)
    result = multi()

    balances = [result[Web3.to_checksum_address(addr)] / 10**decimals for addr in addresses]
    return balances

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
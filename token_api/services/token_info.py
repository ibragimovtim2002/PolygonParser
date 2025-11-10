from web3 import Web3
from .web3_client import w3
import requests

# Минимальный ABI ERC20 для info
ERC20_ABI_INFO = [
    {
        "constant": True,
        "inputs": [],
        "name": "name",
        "outputs": [{"name": "", "type": "string"}],
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "symbol",
        "outputs": [{"name": "", "type": "string"}],
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "totalSupply",
        "outputs": [{"name": "", "type": "uint256"}],
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "decimals",
        "outputs": [{"name": "", "type": "uint8"}],
        "type": "function",
    },
]

def get_token_info(token_address: str) -> dict:
    """
    Получает основную информацию о токене ERC20 по его адресу.

    Args:
        token_address (str): адрес токена ERC20.

    Returns:
        dict: словарь с информацией о токене, содержащий следующие ключи:
            - "name" (str): имя токена.
            - "symbol" (str): символ токена.
            - "totalSupply" (float): общий объём токена с учётом decimals.
            - "decimals" (int): количество десятичных знаков токена.

    Raises:
        ValueError: если адрес токена некорректный или контракт недоступен.
        web3.exceptions.ContractLogicError: при ошибках вызова функций контракта.

    Notes:
        - Использует ABI ERC20_ABI_INFO и объект Web3 `w3`.
        - Преобразует raw totalSupply с учётом decimals для удобства работы.
    """
    addr = Web3.to_checksum_address(token_address)
    contract = w3.eth.contract(address=addr, abi=ERC20_ABI_INFO)

    name = contract.functions.name().call()
    symbol = contract.functions.symbol().call()
    decimals = contract.functions.decimals().call()
    total_supply_raw = contract.functions.totalSupply().call()
    total_supply = total_supply_raw / (10**decimals)

    return {
        "name": name,
        "symbol": symbol,
        "totalSupply": total_supply,
        "decimals": decimals,
    }

def get_top_holders_user_token_thegraph(token_address: str, top_n: int) -> list[tuple[str, float]]:
    """
    Получает топ N держателей токена через The Graph API.

    Args:
        token_address (str): адрес токена
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
    from config import NETWORK, THE_GRAPH_JWT, THE_GRAPH_TOKEN_API_URL
    address = Web3.to_checksum_address(token_address)

    url = f"{THE_GRAPH_TOKEN_API_URL}/v1/evm/holders"
    params = {
        "network": NETWORK,
        "contract": address,
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
        symbol = item["symbol"]
        holders.append((address, balance, symbol))
    return holders


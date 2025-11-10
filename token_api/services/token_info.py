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


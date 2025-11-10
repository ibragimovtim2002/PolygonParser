from web3 import Web3
from config import TOKEN_ADDRESS
from .web3_client import w3

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
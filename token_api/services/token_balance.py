from web3 import Web3
from config import TOKEN_ADDRESS
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
    """
    Получает баланс указанного токена для конкретного адреса в сети Polygon.

    Args:
        address (str): Адрес кошелька пользователя (в формате 0x...).

    Returns:
        dict: Словарь с информацией о балансе токена:
            {
                "address": str,   # исходный адрес
                "balance": float, # баланс токена с учетом десятичных знаков
                "symbol": str     # символ токена (например, "USDC")
            }

    Raises:
        ValueError: Если передан некорректный адрес.
        Exception: При ошибках взаимодействия с контрактом (например, если RPC недоступен).
    """
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
    """
    Получает балансы токена для нескольких адресов.

    Для каждого адреса из списка выполняется запрос к смарт-контракту токена.
    Если адрес некорректен или при запросе произошла ошибка, в список результатов
    добавляется значение `None`.

    Args:
        addresses (list[str]): Список адресов кошельков в формате 0x...

    Returns:
        list[float | None]: Список балансов токена, где каждый элемент соответствует
        адресу из входного списка. Если адрес недействителен или произошла ошибка,
        на его месте будет `None`.

    Raises:
        Exception: Возможные ошибки при взаимодействии с RPC или контрактом токена.
    """
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

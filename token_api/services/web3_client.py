from web3 import Web3
from config import POLYGON_RPC

def connect_polygon() -> Web3:
    """
    Создаёт подключение к сети Polygon через Web3.
    Returns:
        Web3: объект подключения Web3.
    Raises:
        ConnectionError: если не удалось подключиться к сети Polygon.
    """
    w3 = Web3(Web3.HTTPProvider(POLYGON_RPC))
    if not w3.is_connected():
        raise ConnectionError("Не удалось подключиться к сети Polygon")
    return w3

# Инициализация подключения
w3 = connect_polygon()
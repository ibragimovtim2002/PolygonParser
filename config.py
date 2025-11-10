"""
Модуль конфигурации для подключения к сети Polygon и работы с токеном.

Переменные:
- POLYGON_RPC (str): URL RPC-сервера сети Polygon.
- TOKEN_ADDRESS (str): Проверенный (checksum) адрес токена для работы в Web3.
"""

from web3 import Web3

POLYGON_RPC = "https://polygon-rpc.com"
TOKEN_ADDRESS = Web3.to_checksum_address("0x1a9b54a3075119f1546c52ca0940551a6ce5d2d0")
POLYGONSCAN_API_KEY = "GAY4TX7BA1TNKDQ4VNE1GC984JIBZRPIFT"
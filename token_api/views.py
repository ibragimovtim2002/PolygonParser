from rest_framework.decorators import api_view
from rest_framework.response import Response
from .services.token_service import get_balance, get_balances_batch, get_top_holders_thegraph, get_top_with_last_transactions_thegraph

@api_view(["GET"])
def balance_view(request, address):
    """
    API view для получения баланса по адресу в сети.
    Args:
        request (rest_framework.request.Request): объект HTTP-запроса.
        address (str): адрес кошелька для проверки баланса.
    Returns:
        rest_framework.response.Response:
            - В случае успеха: словарь с данными баланса, например {"balance": 123.45}.
            - В случае ошибки: словарь с ключом "error" и описанием ошибки, статус HTTP 400.

    Raises:
        Exception: любые ошибки, возникшие при вызове get_balance, обрабатываются и возвращаются в Response с кодом 400.
    """
    try:
        data = get_balance(address)
        return Response(data)
    except Exception as e:
        return Response({"error": str(e)}, status=400)

@api_view(["POST"])
def balances_batch_view(request):
    """
    Принимает JSON:
    {"addresses": ["0x...", "0x..."]}
    Возвращает JSON:
    {"balances": [0.01, 1000.0]}
    """
    addresses = request.data.get("addresses", [])
    if not isinstance(addresses, list):
        return Response({"error": "addresses должен быть списком"}, status=400)

    balances = get_balances_batch(addresses)
    return Response({"balances": balances})

@api_view(["GET"])
def top_holders_view(request, top_n: int):
    """
    API endpoint для получения топ N держателей токена через The Graph API.

    Args:
        request (rest_framework.request.Request): объект HTTP-запроса.
        top_n (int): количество топ-адресов для получения.

    Returns:
        rest_framework.response.Response:
            - В случае успеха: JSON с ключом "top_holders", содержащим список кортежей (address, balance).
              Пример: {"top_holders": [("0x123...", 100.0), ...]}
            - В случае ошибки: JSON с ключом "error" и описанием ошибки, статус HTTP 400.
    """
    try:
        top = get_top_holders_thegraph(top_n)
        return Response({"top_holders": top})
    except Exception as e:
        return Response({"error": str(e)}, status=400)

@api_view(["GET"])
def top_holders_with_tx_view(request, top_n: int):
    """
    API endpoint для получения топ N держателей токена через The Graph API
    вместе с датой последней транзакции.

    Args:
        request (rest_framework.request.Request): объект HTTP-запроса.
        top_n (int): количество топ-адресов для получения.

    Returns:
        rest_framework.response.Response:
            - В случае успеха: JSON с ключом "top_holders", содержащим список кортежей
              (address, balance, last_tx_date).
              Пример: {"top_holders": [("0x123...", 100.0, "2025-11-10T12:34:56"), ...]}
            - В случае ошибки: JSON с ключом "error" и описанием ошибки, статус HTTP 400.
    """
    try:
        top = get_top_with_last_transactions_thegraph(top_n)
        return Response({"top_holders": top})
    except Exception as e:
        return Response({"error": str(e)}, status=400)


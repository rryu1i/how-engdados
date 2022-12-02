
import requests
import json


def error_check(func):  # passando uma funcao como atributo de uma funcao
    def inner_func(*args, **kargs):
        try:
            func(*args, **kargs)
        except:
            print(f"{func.__name__} falhou")
    return inner_func


@error_check
def cotacao(valor, moeda):
    url = f'https://economia.awesomeapi.com.br/last/{moeda}'
    r = requests.get(url)
    res = json.loads(r.text)[moeda.replace('-','')]
    print(
        f"{valor} {moeda[:3]} hoje custam {float(res['bid']) * valor} {moeda[-3:]}"
    )
    

def main():
    lst_money = [
        "USD-BRL",
        "EUR-BRL",
        "BTC-BRL",
        "RPL-BRL",
        "JPY-BRL",
        "KEK-BRL"
    ]
    for moeda in lst_money:
        cotacao(20,moeda)


if __name__ == '__main__':
    main()

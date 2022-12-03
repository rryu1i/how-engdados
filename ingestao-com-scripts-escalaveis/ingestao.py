import requests
import logging
from abc import abstractmethod

logger = logging.getLogger(__name__)  # nome do script (ingestao)
logging.basicConfig(level=logging.INFO)


class MercadoBitcoinApi():

    def __init__(self, coin:str) -> None:
        self.coin = coin
        self.base_endpoint = "https://www.mercadobitcoin.net/api"

    @abstractmethod  # pois sabemos que o metodo devera ser extendido
    def _get_endpoint(self):
        pass

    
    def get_data(self) -> dict:
        endpoint = self._get_endpoint()
        logger.info(f"Getting data from endpoint: {endpoint}")
        response = requests.get(endpoint)
        response.raise_for_status()  # levanta exception se nao iniciar com2
        return response.json()

class BtcApi(MercadoBitcoinApi):

    def _get_endpoint(self):
        return "a"

BtcApi(coin="BTC")



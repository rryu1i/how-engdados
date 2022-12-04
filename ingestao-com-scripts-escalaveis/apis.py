import os
import requests
import logging
from abc import ABC, abstractmethod
import datetime
from typing import List
import json
import schedule
import time
from backoff import on_exception, expo
from ratelimit import limits, RateLimitException

logger = logging.getLogger(__name__)  # nome do script (ingestao)
logging.basicConfig(level=logging.INFO)



class MercadoBitcoinApi(ABC):


    def __init__(self, coin:str) -> None:
        self.coin = coin
        self.base_endpoint = "https://www.mercadobitcoin.net/api"


    @abstractmethod  # pois sabemos que o metodo devera ser extendido
    def _get_endpoint(self, **kwargs) -> str:  # python entende que a assinatura dessa funcao pode receber qualquer tipo de argumento do tipo chave valor
        pass

    
    @on_exception(expo, RateLimitException, max_tries=10)
    @limits(calls=29, period=38)
    @on_exception(expo, requests.exceptions.HTTPError, max_tries=10)
    def get_data(self, **kwargs) -> dict:
        endpoint = self._get_endpoint(**kwargs)
        logger.info(f"Getting data from endpoint: {endpoint}")
        response = requests.get(endpoint)
        response.raise_for_status()  # levanta exception se nao iniciar com2
        return response.json()


class DaySummaryApi(MercadoBitcoinApi):
    type = "day-summary"


    def _get_endpoint(self, date: datetime.date):
        return f"{self.base_endpoint}/{self.coin}/{self.type}/{date.year}/{date.month}/{date.day}"


class TradesApi(MercadoBitcoinApi):
    type = "trades"


    def _get_unix_epoch(self, date: datetime.date) -> int:  # principio da responsabilidade
        return int(date.timestamp())


    def _get_endpoint(self, date_from: datetime.date = None, date_to: datetime.date = None) -> str:
        if date_from and not date_to:
            unix_date_from = self._get_unix_epoch(date_from)
            endpoint = f"{self.base_endpoint}/{self.coin}/{self.type}/{unix_date_from}"
        if date_from and date_to:
            unix_date_from = self._get_unix_epoch(date_from)
            unix_date_to = self._get_unix_epoch(date_to)
            endpoint = f"{self.base_endpoint}/{self.coin}/{self.type}/{unix_date_from}/{unix_date_to}"
        else:
            endpoint = f"{self.base_endpoint}/{self.coin}/{self.type}"
        return endpoint
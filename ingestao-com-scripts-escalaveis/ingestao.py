import os
import requests
import logging
from abc import ABC, abstractmethod
import datetime
from typing import List
import json


logger = logging.getLogger(__name__)  # nome do script (ingestao)
logging.basicConfig(level=logging.INFO)


class MercadoBitcoinApi(ABC):

    def __init__(self, coin:str) -> None:
        self.coin = coin
        self.base_endpoint = "https://www.mercadobitcoin.net/api"

    @abstractmethod  # pois sabemos que o metodo devera ser extendido
    def _get_endpoint(self, **kwargs) -> str:  # python entende que a assinatura dessa funcao pode receber qualquer tipo de argumento do tipo chave valor
        pass

    
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

print(DaySummaryApi(coin="BTC").get_data(date=datetime.date(2021,6,21)))





class TradesApi(MercadoBitcoinApi):
    type = "trades"

    def _get_unix_epoch(self, date: datetime) -> int:  # principio da responsabilidade
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


class DataTypeNotSupportedForIngestionException(Exception):
    def __init__(self, *args: object) -> None:
        self.data = data
        self.message = f"Data type {type(data)} is not supported for ingestion"
        super().__init__(self.message)


class DataWriter:

    def __init__(self, coin: str, api:str) -> None:
        self.coin = coin
        self.api = api
        self.filename = f"{self.api}/{self.coin}/{datetime.datetime.now()}.json"

    def _write_row(self, row: str) -> None:
        os.makedirs(os.path.dirname(self.filename), exist_ok = True)
        with open(self.filename, "a") as f:  # append
            f.write(row)

    def write(self, data: [List, dict]):  # pois TradesApi nos retorna um lista de dicts, diferente de DaySummary que e so dict
        if isinstance(data, dict):  # verifica se o objeto que e passado e uma instancia de uma determinada class
            self._write_row(json.dumps(data) + "\n")
        elif isinstance(data,list):
            for element in data:
                self.write(element)  # funcao recursiva, e se tiver uma lista dentro de uma lista?
        else:
            raise DataTypeNotSupportedForIngestionException(data)



# data = DaySummaryApi("BTC").get_data(date=datetime.date(2021,6,21))
# writer = DataWriter("day_summary.json")
# writer.write(data)


# data = TradesApi("BTC").get_data()
# writer = DataWriter("trades.json")
# writer.write(data)


class DataIngestor(ABC):

    def __init__(self, writer: DataWriter, coins: List[str], default_start_date: datetime.datetime) -> None:
        self.coins = coins
        self.default_start_date = default_start_date
        self.writer = writer


    @abstractmethod  # queremos um metodo abstrato, pois temos duas apis, summary e trade, por motivos de escalabilidade e melhor reecrevelos
    def ingest(self) -> None:
        pass


class DaySummaryIngestor(DataIngestor):
    def ingest(self) -> None:
        date = self.default_start_date
        if date < datetime.date.today():
            for coin in self.coins:
                api = DaySummaryApi(coin=coin)
                data = api.get_data(date=date)
                self.writer(coin=coin, api=api.type).write(data)
                # atualizar a data

ingestor = DaySummaryIngestor(writer=DataWriter, coins=["BTC", "ETH", "LTC"], default_start_date=datetime.date(2021,6,1))
ingestor.ingest()
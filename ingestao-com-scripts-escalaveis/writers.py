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

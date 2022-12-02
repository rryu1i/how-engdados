import datetime
import math
from typing import List


class Pessoa:
    def __init__(self, nome: str, sobrenome: str, data_de_nascimento: datetime.date) -> None:
        self.nome = nome
        self.sobrenome = sobrenome
        self.data_de_nascimento = data_de_nascimento

    @property
    def idade(self) -> int:
        return math.floor((datetime.date.today() - self.data_de_nascimento).days / 365.2425)

    def __str__(self) -> str:
        return f"{self.nome} {self.sobrenome} tem {self.idade} anos"


class Curriculo:
    def __init__(self, pessoa: Pessoa, experiencias: List[str]) -> None:
        self.pessoa = pessoa
        self.experiencias = experiencias


    @property
    def quantidade_de_experiencias(self) -> int:
        return len(self.experiencias)

    
    @property
    def empresa_atual(self) -> str:
        return self.experiencias[-1]

    
    def adiciona_experiencia(self, experiencia: str) -> None:
        self.experiencias.append(experiencia)

    
    def __str__(self) -> str:
        return f"{self.pessoa.nome} {self.pessoa.sobrenome} tem {self.pessoa.idade} anos e ja trabalhou em {self.quantidade_de_experiencias} empresas" \
                f" e atualmente trabalha na {self.empresa_atual}"


roger = Pessoa(nome="Roger", sobrenome="Issonaga", data_de_nascimento=datetime.date(1998,12,16))

curriculo_roger = Curriculo(pessoa=roger, experiencias=["UTFPR", "PADO S/A"])

curriculo_roger.adiciona_experiencia("???")

print(curriculo_roger)


class Vivente:
    def __init__(self, nome: str, data_de_nascimento: datetime.date) -> None:
        self.nome = nome
        self.data_de_nascimento = data_de_nascimento

    
    @property
    def idade(self) -> int:
        return math.floor((datetime.date.today() - self.data_de_nascimento).days / 365.2425)


    def emite_ruido(self, ruido: str):
        print(f"{self.nome} fez ruido: {ruido}")


class PessoaHeranca(Vivente):
    def __str__(self) -> str:
        return f"{self.nome} tem {self.idade} anos"

    
    def fala(self, frase):
        return self.emite_ruido(frase)


class Cachorro(Vivente):
    def __init__(self, nome: str, data_de_nascimento: datetime.date, raca: str) -> None:
        super().__init__(nome, data_de_nascimento)
        self.raca = raca


    def __str__(self) -> str:
        return f"{self.nome} e da raca {self.raca} e tem {self.idade} anos"    

    
    def late(self):
        return self.emite_ruido("Meow!")


roger2 = PessoaHeranca(nome="Roger", data_de_nascimento=datetime.date(1998,12,16))

print(roger2)

cachorro = Cachorro(nome="Gato", data_de_nascimento=datetime.date(2020,1,1),raca="kek")

print(cachorro)

cachorro.late()
roger2.fala("zzz")
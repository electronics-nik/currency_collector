from abc import ABC, abstractmethod

class Collector(ABC):
    def __init__(self, url):
        self.url = url

    @abstractmethod
    def collect(self, currencies_code: dict[str, int]):
        return {}

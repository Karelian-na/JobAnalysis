import abc
from src.models.entities import EntityBase


class BaseService:
    @abc.abstractmethod
    def getById(self, ID: int) -> EntityBase:
        pass

    @abc.abstractmethod
    def getAll(self) -> list[EntityBase]:
        pass

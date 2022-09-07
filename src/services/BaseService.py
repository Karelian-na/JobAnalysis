import abc
from models.entities import EntityBase

class BaseService:
	@abc.abstractmethod
	def getById(self, id: int) -> EntityBase:
		pass

	@abc.abstractmethod
	def getAll(self) -> list[EntityBase]:
		pass
from models.entities import Job, engine
from services.BaseService import BaseService
from sqlalchemy.orm import sessionmaker

session = sessionmaker(engine).__call__()

class JobService(BaseService):
	def getById(self, id: int) -> Job | None:
		"""get a job from database

		Args:
			id (int): the job id

		Returns:
			Job | None: if the database has the job, return the job object, otherwise, None
		"""
		return session.query(Job).filter(Job.id == id).one_or_none()

	def gedAllByName(self, name: str) -> list[Job] | None:
		"""get all jobs from database which name is name

		Args:
			name (str): the job name

		Returns:
			typing.List[Job] | None: if has, return a list of Job, otherwise None
		"""
		jobs = session.query(Job).filter(Job.name == name).all()
		if jobs.__len__ == 0:
			return None
		else:
			return jobs

	def getAll(self) -> list[Job] | None:
		"""get all record from database, user with caution

		Returns:
			list[Job] | None: if database is empty, return None, otherwise the all jobs
		"""
		jobs = session.query(Job).all()
		if jobs.__len__ == 0:
			return None
		else:
			return jobs
import re
from models.entities import Job
from nltk.corpus import stopwords
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import confusion_matrix, accuracy_score

class JobAnalysis:
	def statistic(self, jobs: list[Job], mainField: str, subField: str = None) -> list:
		"""statistic the jobs data by mainField and subField

		Args:
			jobs (list[Job]): the data
			mainField (str): the main field of Job
			subField (str, optional): the sub field of Job. Defaults to None.

		Raises:
			Exception: raise Exception when the passed field is not in Job

		Returns:
			list: the result
		"""

		if hasattr(Job, mainField) == None or (subField and hasattr(Job, subField)):
			raise Exception("{} field is not in Job".format(mainField or subField))

		regex = re.compile("((（|\(|\[).*(）|\]|\)))|((-|\+).*)|[\d]届?(.招)?")
		x = [ regex.sub("", job.name) for job in jobs]

		# x = [ job.name for job in jobs]
		vectorizer = TfidfVectorizer(max_features=10)
		X = vectorizer.fit_transform(x).toarray()
		res = vectorizer.get_feature_names_out()
		print(res)

		# x_train, x_test, y_train, y_test = train_test_split(X, x, test_size=0.3, random_state=2019071190)
		# classifier = RandomForestClassifier(random_state=2019071190)
		# classifier.fit(x_train, y_train)
		# y_pred = classifier.predict(x_test)
		# print(accuracy_score(y_test, y_pred))
		
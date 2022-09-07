
DB_HOST = "127.0.0.1"
DB_NAME = "jobAnalysis"
DB_USER = "user"
DB_PWD = "123456"
DB_PORT = 3306

DB_URL = "mysql+mysqldb://{}:{}@{}:{}/{}".format(
	DB_USER,
	DB_PWD,
	DB_HOST,
	DB_PORT,
	DB_NAME
)
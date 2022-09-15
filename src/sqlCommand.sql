CREATE DATABASE `jobAnalysis`;
CREATE USER `user`@`%` IDENTIFIED BY '123456';
GRANT Alter, Alter Routine, 
	Create, Create Routine, 
	Create Temporary Tables, 
	Create View, Delete, 
	Drop, Event, Execute, 
	Grant Option, Index, Insert, 
	Lock Tables, References, Select, 
	Show View, Trigger, 
	Update ON `jobanalysis`.* TO `user`@`%`;

USE `jobAnalysis`;

CREATE TABLE jobs(
	id VARCHAR(28) PRIMARY KEY,
	name VARCHAR(255),
	salary_min TINYINT,
    salary_max TINYINT,
    salary_sys TINYINT,
	work_area VARCHAR(255),
	experience VARCHAR(255),
	degree VARCHAR(255),
	company_name VARCHAR(255),
	type VARCHAR(255)
);

SELECT * FROM jobs WHERE salary_max < salary_min

SELECT degree FROM jobs GROUP BY degree

SELECT experience FROM jobs GROUP BY experience
SELECT type FROM jobs GROUP BY type

SELECT * FROM jobs WHERE id = "000ff605dd5b84991XB-09u0F1NW"

SELECT * FROM jobs WHERE experience = "大专"
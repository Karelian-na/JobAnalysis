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
	id INT PRIMARY KEY AUTO_INCREMENT,
	name VARCHAR(255),
	salary VARCHAR(20),
	city VARCHAR(255),
	experience VARCHAR(255),
	degree VARCHAR(255),
	company_name VARCHAR(255),
	type VARCHAR(255)
);
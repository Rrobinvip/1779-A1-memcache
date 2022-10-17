# ECE 1779 A1 MEMCACHE - Group 17

## To create environment:
1. Create the environment from the `environment.yml` with `conda env create -f environment.yml`
1. Activate the new environment with `conda activate <name_env>`, in this case, the `<name_env>` is `MEMCACHE`
3. Inspect packages with `conda list`

## To run:
1. At base dir
`python3 run.py`

## 5 key components:
1. The web browser that initiates requests
2. The web front end that manages requests and operations
3. The local file system where all data is stored
4. The mem-cache that provides faster access
5. The relational database (RDBMS), which stores a list of known keys, the configuration parameters, and other important values.

### Database Schema
1.	Command Create Database: `Create Database If Not Exists cloudcomputing`
2.	Select the Database: `Use cloudcomputing`
3.	Create Tables:
	Table configuration:
	`Create Table If Not Exists configuration(id INT NOT NULL AUTO_INCREMENT,capacity INT NOT NULL,replacePolicy TINYINT NOT NULL,CONSTRAINT configuration_pk PRIMARY KEY(id));`
	Table statistics:
	`Create Table If Not Exists statistics(id INT NOT NULL AUTO_INCREMENT, itemNum INT NOT NULL, itemSize FLOAT NOT NULL, requestNum INT NOT NULL, missRate FLOAT NOT NULL, hitRate FLOAT NOT NULL, CONSTRAINT statistics_pk PRIMARY KEY(id));`

For more easily access, when terminal is at the project base dir, after creating and use the databse, run `source database.sql`. All tables will be created.
Remember to change the database config for local database connection.


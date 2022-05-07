# Backend zum Portfolio Manager

## Motivation and Goal
The Repository is the backend for the main application ([Frontend](https://github.com/Pondo18/stock-portfolio-manager-frontend)). It works as a Rest-API, which should query data from a MySQL DB.


## Implementation
The Rest-API is implemented with via Flask.


## Dependencies
- Python 3 is installed 

~~~~Bash
# Installing the pip dependencies from the requirements.txt
pip install -m requirements.txt
~~~~

## Deployment 

For deploying the MySQL DB a docker-compose file is placed in the root dir.

~~~~Bash
# Starting the docker container
docker-compose up -d
~~~~

The table structure necessary for the application to works, needs to be created.

~~~~SQL
CREATE TABLE `holdings` (
  `id` int NOT NULL,
  `username` varchar(20) NOT NULL,
  `holding` varchar(100) NOT NULL,
  `number` int NOT NULL,
  `buyIn` double NOT NULL,
  `buyDate` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
ALTER TABLE `holdings`
  ADD PRIMARY KEY (`id`);
ALTER TABLE `holdings`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

CREATE TABLE `userdata` (
  `hashcode` varchar(32) NOT NULL,
  `username` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `credits` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
ALTER TABLE `userdata`
  ADD PRIMARY KEY (`username`);
~~~~

The credentials for the database should be stored in environment variables or set via default values in the config.py

~~~~Bash
# env variables to set

DBHOST
DBUSER
DBNAME
DBPASS
~~~~

Mithilfe dem Folgenden kann zwischen lokaler und nicht lokaler Datenbank gewechselt werden.
~~~~Bash
source local.env
~~~~
oder:
~~~~Bash
source production.env
~~~~

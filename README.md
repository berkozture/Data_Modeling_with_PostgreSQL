This is a project I completed for Udacity's Data Engineering nanodegree program. The scenario is as follows:

The startup Sparkify aims to analyse the data they've been collecting on songs and user activity on their new music streaming app. In order to understand what songs the users are listening to and to optimize the queries in doing so, this projects creates a star schema out of two datasets. 


In order to create and populate the tables, follow the steps below:
- Run create_tables.py
- Run etl.py
These files can be run from the terminal.


create_tables.py
- The Python file create_tables.py drops and creates these tables. This file can be run to reset the tables before each time the ETL scripts are run.

etl.py
- etl.py reads and processes files from song_data and log_data and loads them into the tables. 

sql_queries.py
- sql_queries.py contains all the sql queries to create and insert data into the tables.


The star schema should consist of a fact table (songplays) and four dimension tables (users, songs, artists, time). Star schemas make the queries easier with simple JOINS, and allow for fast aggregations. As the analysis of user activity will require performing of aggregations (and not necessarily require tables in the 3NF form), the schema was designed in a star schema.

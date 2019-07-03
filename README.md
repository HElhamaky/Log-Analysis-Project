
# Logs Analysis Project

Building an informative summary from logs by SQL database queries. Interacting with a live database both from the command line and from the python code. This project is a part of the Udacity's Full Stack Web Developer Nanodegree.  

## Technologies used

1. PostgreSQL
2. Writing Python code with DB-API
3. Linux-based virtual machine (VM) Vagrant

  
## Project Requirements

Creating a reporting tool that prints out reports (in plain text) based on the data in the database. This reporting tool is a Python program using the ```psycopg2``` module to connect to the database.

The reporting tool should answer three questions >>>

1. What are the most popular three articles of all time?
2. Who are the most popular article authors of all time?
3. On which days did more than 1% of requests lead to errors?

* Project follows good SQL coding practices: Each question should be answered with a single database query.
* The code is error free and conforms to the PEP8 style recommendations.
* The code presents its output in clearly formatted plain text.


## System setup and how to view this project

This project makes use of Udacity's Linux-based virtual machine (VM) configuration which includes all of the necessary software to run the application.

  

1. Download [Vagrant](https://www.vagrantup.com/) and install.
2. Download [Virtual Box](https://www.virtualbox.org/) and install.
3. Clone this [repository](https://github.com/udacity/fullstack-nanodegree-vm). to a directory of your choice.
4. Download the **newsdata.sql** (extract from **newsdata.zip** (not provided here though)) and **newsdata.py** files from the respository and move them to your **vagrant** directory within your VM.

  
#### Run these commands from the terminal in the folder where your vagrant is installed in:


1.  ```vagrant up``` to start up the VM.
2.  ```vagrant ssh``` to log into the VM.
3.  ```cd /vagrant``` to change to your vagrant directory.
4.  ```psql -d news -f newsdata.sql``` to load the data and create the tables.
5.  ```python logresults.py``` to run the reporting tool.

  
## Created Views

#### Top Popular Articles

  
````sql
CREATE VIEW top_popular_articles as
SELECT articles.title, count(log.path) as article_views
FROM articles, log
WHERE  log.path  LIKE  '%' || articles.slug
AND  log.status='200 OK'
GROUP BY articles.title
ORDER BY article_views desc
LIMIT  3;
````

  
#### Most Popular Author

````sql
CREATE VIEW most_popular_author as
SELECT authors.name, count(log.path) as author_views
FROM authors, articles, log
WHERE  status != '404 NOT FOUND'
AND articles.author = authors.id
AND  log.path  LIKE  '%' || articles.slug
GROUP BY authors.name
ORDER BY author_views desc;
````

  
#### Date / Status View

````sql
CREATE VIEW date_status AS
SELECT  time ::date,status
FROM  log;
````

#### Failed Status

````sql
CREATE VIEW failed_status AS
SELECT  time,
count(*) AS num
FROM date_status
WHERE  status = '404 NOT FOUND'
GROUP BY  time;
````

#### All Status Count

````sql
CREATE VIEW all_status AS
SELECT  time,
count(*) AS num
FROM date_status
WHERE  status = '404 NOT FOUND'
OR  status = '200 OK'
GROUP BY  time;
````


#### Top Percentage Error

````sql
CREATE VIEW errorpercent AS
SELECT all_status.time,
all_status.num AS statall,
failed_status.num AS statfailed,
failed_status.num::double precision/all_status.num::double precision * 100  AS percentagefailed
FROM all_status,failed_status
WHERE all_status.time = failed_status.time;
````


## Helpful Resources

*  [Python 3](https://www.python.org/download/releases/3.0/) - The code uses ver 3.6.4

*  [Vagrant](https://www.vagrantup.com/) - A virtual environment builder and manager

*  [VirtualBox](https://www.virtualbox.org/) - An open source virtualiztion product.

*  [Git](https://git-scm.com/) - An open source version control system

*  [PEP 8 -- Style Guide for Python Code](https://www.python.org/dev/peps/pep-0008/)

*  [PostgreSQL 9.5 Documentation](https://www.postgresql.org/docs/9.5/static/index.html)


## Citation and Attribution

In order to complete this project I have looked at some repositories, listed below.
* [logs-analysis-project](https://gitlab.com/SDey96/logs-analysis-project/tree/master) by @SDey96
* [Udacity-Logs-Analysis-Full-Stack-Web-Developer-Nanodegree-Program](https://github.com/khushkoolkhosla/Udacity-Logs-Analysis-Full-Stack-Web-Developer-Nanodegree-Program-) by @khushkoolkhosla
* [Udacity-log-analysis-project](https://github.com/luckyrose89/Udacity-log-analysis-project) by @luckyrose89
* [udacity-fsnd-log-analysis](https://github.com/shauryashahi/udacity-fsnd-log-analysis) by @shauryashahi
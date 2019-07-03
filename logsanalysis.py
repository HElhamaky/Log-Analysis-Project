#!/usr/bin/env python

import psycopg2

DBNAME = "news"

request_1 = "what are the most popular articles of all time?"
query_1 = ("select * from top_popular_articles;")

request_2 = "who are the most popular article authors of all time?"
query_2 = ("select * from most_popular_author;")

request_3 = "On which days did more than 1% of the requests led to error?"
query_3 = ("select time, round(percentagefailed) as percent \n"
           "from errorpercent \n"
           "where errorpercent.percentagefailed > 1;")


def make_query(query):
    try:
        db = psycopg2.connect(database=DBNAME)
        c = db.cursor()
        c.execute(query)
        return c.fetchall()
        db.close()
    except psycopg2.error as e:
        print("Unable to connect to the database")
        print(e.pgerror)
        print(e.diag.message_detail)
        sys.exit(1)

result1 = make_query(query_1)
result2 = make_query(query_2)
result3 = make_query(query_3)


def print_results(query_list):
    for i in range(len(query_list)):
        col1 = query_list[i][0]
        col2 = query_list[i][1]
        print("\t" + "%s - %d" % (col1, col2) + "views")
    print("\n")


print(request_1)
print_results(result1)
print(request_2)
print_results(result2)
print(request_3)
print("\t" + str(result3[0][0]) + " - " + str(result3[0][1]) + "% errors")

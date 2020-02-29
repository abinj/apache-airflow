import os
from datetime import timedelta, datetime

# [START import_module]
# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG
# Operators; we need this to operate!
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from textblob import TextBlob as tb
import re
import feedparser


# [END import_module]

# [START default_args]
# These args will get passed on to each operator
# You can override them on a per-task basis during operator initialization
from pymongo import MongoClient

format = "%a, %d %b %Y %H:%M:%S %Z"


def rss_feed_scraper(url, source):
    feeds = []

    feed = feedparser.parse(url)

    # number of stories
    numStories = len(feed['entries'])

    # list to contain polarity of stories
    # final = []

    for i in range(0, numStories):
        # print(feed['entries'][i])
        # initial description
        descInit = feed['entries'][i]['summary_detail']['value']
        # cleaning out the img tag
        # descClean = re.sub('\<img.*$', '', descInit)
        cleanr = re.compile('<.*?>')
        descClean = re.sub(cleanr, '', descInit)
        # final description
        desc = tb(descClean)
        print("Description >>>>>>>>>>>>>>>>>>>>")
        print(desc)
        # title of the entry
        title = tb(feed['entries'][i]['title'])
        # final string which contains description and headline to get a better polarity result
        if not title.ends_with("."):
            title = title + "."
        completeString = title + " " + desc
        print("Complete String >>>>>>>>>>>>>>>>")
        print(completeString)
        pub_date = ""
        try:
            pub_date = tb(feed['entries'][i]['published'])
            print(pub_date)
        except:
            print("No Publish Date")

        if pub_date is not "":
            feeds.append({"Text": str(completeString), "date": datetime.strptime(str(pub_date), format)
                                , "title": str(title), "description": str(desc), "source": source})
    print("<<<<<<   Count >>>>>>  " + str(len(feeds)))
        # appending story headline and description polarity to final list
        # final.append(completeString.sentiment.polarity)

    # polarity calculations
    # finalPolarity = sum(final) / len(final)
    # print(min(final))
    # worstPolarity = final.index(min(final))
    # print(max(final))
    # bestPolarity = final.index(max(final))

    # print(finalPolarity)
    # print(worstPolarity)
    # print(bestPolarity)




default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'default_timezone': "EST",
    'start_date': datetime(2020, 2, 28, 2),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(hours=5),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
    # 'wait_for_downstream': False,
    # 'dag': dag,
    # 'sla': timedelta(hours=2),
    # 'execution_timeout': timedelta(seconds=300),
    # 'on_failure_callback': some_function,
    # 'on_success_callback': some_other_function,
    # 'on_retry_callback': another_function,
    # 'sla_miss_callback': yet_another_function,
    # 'trigger_rule': 'all_success'
}
# [END default_args]

# [START instantiate_dag]
dag = DAG(
    'news_fetch',
    default_args=default_args,
    description='News Fetch DAG',
    schedule_interval=timedelta(hours=5),
)
# [END instantiate_dag]

# t1 and t2 are examples of tasks created by instantiating operators
# [START basic_task]
t1 = PythonOperator(
    task_id='fox_news_parser',
    depends_on_past=False,
    python_callable=rss_feed_scraper,
    op_kwargs={'url': "http://rss.cnn.com/rss/cnn_topstories.rss", 'source': 'foxnews'},
    # retries=3,
    dag=dag,
)

t2 = PythonOperator(
    task_id='cnn_news_parser',
    depends_on_past=False,
    python_callable=rss_feed_scraper,
    op_kwargs={'url': "http://feeds.foxnews.com/foxnews/latest", 'source': 'cnn'},
    # retries=3,
    dag=dag,
)


# [END basic_task]

# [START documentation]
# dag.doc_md = __doc__
#
# t1.doc_md = """\
# #### Task Documentation
# You can document your task using the attributes `doc_md` (markdown),
# `doc` (plain text), `doc_rst`, `doc_json`, `doc_yaml` which gets
# rendered in the UI's Task Instance Details page.
# ![img](http://montcs.bloomu.edu/~bobmon/Semesters/2012-01/491/import%20soul.png)
# """
# [END documentation]

# [START jinja_template]
# templated_command = """
# {% for i in range(5) %}
#     echo "{{ ds }}"
#     echo "{{ macros.ds_add(ds, 7)}}"
#     echo "{{ params.my_param }}"
# {% endfor %}
# """
#
# t3 = BashOperator(
#     task_id='templated',
#     depends_on_past=False,
#     bash_command=templated_command,
#     params={'my_param': 'Parameter I passed in'},
#     dag=dag,
# )
# [END jinja_template]
#
# t1, t2
# [END tutorial]
# t1, t2
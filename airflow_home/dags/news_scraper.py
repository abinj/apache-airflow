import datetime

import feedparser
from textblob import TextBlob as tb
import re
from pymongo import MongoClient

format = "%a, %d %b %Y %H:%M:%S %Z"
client = MongoClient('mongodb+srv://abi0708:learn4fun@cluster0-wht0f.mongodb.net/bdat_sdm?retryWrites=true&w=majority')



def rss_feed_scraper(url):
    feeds = []
    source = "cnn"

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
            feeds.append({"Text": completeString, "date": datetime.datetime.strptime(str(pub_date), format)
                             , "title": title, "description": desc, "source": source})
    # client.bdat_sdm.news.insert_many(feeds)
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

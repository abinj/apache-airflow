import feedparser
from textblob import TextBlob as tb
import re

url = "http://rss.cnn.com/rss/cnn_topstories.rss"
feed = feedparser.parse(url)

# number of stories
numStories = len(feed['entries'])

# list to contain polarity of stories
final = []

for i in range(0,numStories):
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
    # appending story headline and descrition polarity to final list
    final.append(completeString.sentiment.polarity)

# polarity calculations
finalPolarity = sum(final)/len(final)
print(min(final))
worstPolarity = final.index(min(final))
print(max(final))
bestPolarity = final.index(max(final))

print(finalPolarity)
print(worstPolarity)
print(bestPolarity)
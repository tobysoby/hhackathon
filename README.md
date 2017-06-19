# Mining deutsche welle facebook posts

repo for the fjp hackathon 06/12/2017 in Hamburg

## Idea

deutsche welle is a german public news outlet for an international audience. 
The publishing company is financed by the German State Department and should adress its international audience by providing international news.
The hackathon project tries to help to accomplish this mission by delivering meta information on facebook posts by deutschewellenews. The goal is to answer questions such as

* is deutschewellenews fulfilling its mission to provide globalized news? what regions are the facebook-posts covering?
* which persons were covered?
* which cities?

Future:
* how to people react to certain posts (in terms of sentiment?)?
* can these informations be provided instantly?

Since we only had limited time, we concentrated on the first three questions. We answer them by using the facebook graph api and text-mining techniques such as Named Entity Recognition. We try to use a easy-to-use graph building framework to make it possible for data journalists to easily provide the insights generated by our data generation framework.

## Prerequisites

* Python 2.7
* Pandas, Spacy (including the language models), Geotext, Seaborn
* d3.js (javascript) or DataWrapper

## Structure

We used Python to get and analyze the data. The data was provided as a .json by the Facebook Graph API. We load the data into pandas dataframe, apply Named Entity Recognition provided by Spacy, built some graphs with seaborn. To build an interactive map representing the places the facebook posts were about we show the ability to use the user (and journalist) -friendly tool datawrapper.

We decided to publish the complete (original) jupyter notebook developed during the day at the fjp hackathon. It can be found in the notebook folder. Please consider the "hacky" atmosphere during such an event. Additionally, we afterwards provided a full script automating the process. The next step would be to deploy a python server generating the data real time.

## Outcome

After saving the data, the data was loaded into a d3.js script partly provided by datawrapper.
The result can be viewed under

https://datawrapper.dwcdn.net/eIXtj/2/

The script showed how to pull data out of facebook, transform it, enrich it with additional text data and publish it using an easy-to-use tool.

## Links

Facebook Graph API: https://developers.facebook.com/docs/graph-api
Python: https://www.python.org/
Pandas: http://pandas.pydata.org/
Seaborn: https://seaborn.pydata.org/
d3.js: https://d3js.org/
DataWrapper: https://www.datawrapper.de/

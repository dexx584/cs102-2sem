from bottle import (
    route, run, template, request, redirect
)

from scrapper import get_news
from db import News, session
from bayes import NaiveBayesClassifier


@route("/news")
def news_list():
    s = session()
    rows = s.query(News).filter(News.label == None).all()
    return template('news_template', rows=rows)


@route("/add_label/")
def add_label():
    # PUT YOUR CODE HERE
    lbl = request.query["label"]
    id = request.query["id"]
    _session = session()
    s = _session.query(News).get(id)
    s.lbl = lbl
    _session.add(s)
    _session.commit()
    redirect("/news")


@route("/update")
def update_news():
    # PUT YOUR CODE HERE
    _session = session()
    link = get_news("https://news.ycombinator.com/newest", 1)
    for i in range(len(link)):
        a = News(title=link[i]["title"], author=author[i]["author"],
                 comments=link[i]["comments"], points=link[i]["points"],
                 url=link[i]["url"])
        if (_session.query(News).filter(News.tittle == a.title and News.author == a.author).count()) == 0:
            _session.add(a)
    _session.commit()
    redirect("/news")


@route("/classify")
def classify_news():
    # PUT YOUR CODE HERE


if __name__ == "__main__":
    run(host="localhost", port=8080)


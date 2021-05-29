import requests
from bs4 import BeautifulSoup


def extract_news(parser):
    """ Extract news from a given web page """
    # PUT YOUR CODE HERE
    new_list = []
    _l = []
    table = parser.body.center.table
    for i in table.findAll("tr"):
        _l.append(i)
    body = _l[3].findAll("tr")
    for i in range(0, len(body) - 2, 3):
        dictionary = dict()
        links = body[i + 1].findAll("td")[1].findAll("a")
        if (len(links) < 4) or (len(links) > 4):
            continue
        dictionary["points"] = int(body[i + 1].findAll("td")[1].span.text.split()[0])
        dictionary["author"] = links[0].text
        comment = "discuss"
        if len(links) == 4:
            comment = links[3].text.split()[0]
        if comment == "discuss":
            dictionary["comments"] = 0
        else:
            dictionary["comments"] = len(comment)
        td = body[i].findAll("td")[2]
        td = td.find("a")
        dictionary["url"] = td["href"]
        dictionary["title"] = td.text
        new_list.append(dictionary)
    return new_list


def extract_next_page(parser):
    """ Extract next page URL """
    # PUT YOUR CODE HERE
    array = []
    for i in parser.body.center.table.findAll("tr"): array.append(i)
    body = array[3].findAll("tr")
    if (len(body) < 92): return "newest"
    return body[-1].findAll("td")[1].find("a")["href"]


def get_news(url, n_pages=1):
    """ Collect news from a given web page """
    news = []
    while n_pages:
        print("Collecting data from page: {}".format(url))
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        news_list = extract_news(soup)
        next_page = extract_next_page(soup)
        url = "https://news.ycombinator.com/" + next_page
        news.extend(news_list)
        n_pages -= 1
    return news


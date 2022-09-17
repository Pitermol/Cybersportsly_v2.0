import requests
from lxml import html, etree

cur_heroes_dire = ['Abaddon', 'Alchemist', 'Ancient Apparition', 'Anti-Mage', 'Arc Warden']
cur_heroes_rad = ['Beastmaster', 'Bloodseeker', 'Bounty Hunter', 'Brewmaster', 'Bristleback']

def calculate(cur_heroes_rad, cur_heroes_dire):
    with requests.Session() as s:
        url = "https://counterpick.herokuapp.com/?"
        for i in cur_heroes_dire:
            url += f"heroes[]={i}&"
        url = url[:-1]
        content = s.get(url, proxies= {"http": "http://172.67.176.9:80"}, timeout=10)
        print("done")
        s.close()
        print(content)

    tree = html.fromstring(content.text)
    plus = tree.xpath("//div[@id = \"good-picks\"]/div")
    minus = tree.xpath("//div[@id = \"bad-picks\"]/div")
    points = 0
    for hero in cur_heroes_rad:
        # print(list(map(lambda x: str(x.xpath(".//h3")[0].text), plus)))
        # print(list(map(lambda x: str(x.xpath(".//h3")[0].text), minus)))
        item = list(filter(lambda x: str(x.xpath(".//h3")[0].text) == hero, plus))
        if len(item) == 1:
            item = item[0]
            point = float(str(etree.tostring(item, pretty_print=True)).split("rating: ")[1].split(" (")[0])
            points += point
        else:
            item = list(filter(lambda x: str(x.xpath(".//h3")[0].text) == hero, minus))
            if len(item) == 1:
                item = item[0]
                point = float(str(etree.tostring(item, pretty_print=True)).split("rating: ")[1].split(" (")[0])
                points += point

    return points


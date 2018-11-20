import requests, json, pytz, os
from bs4 import BeautifulSoup
from datetime import datetime
from dotenv import load_dotenv
from requests_oauthlib import OAuth1Session


# .envファイルから各種変数を取得
dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path)

CONSUMER_KEY = os.environ["CONSUMER_KEY"]
CONSUMER_SECRET = os.environ["CONSUMER_SECRET"]
ACCESS_KEY = os.environ["TOKEN"]
ACCESS_SECRET = os.environ["TOKEN_SECRET"]
GitHub_ACCOUNT = os.environ["GitHub_ACCOUNT"]
Twitter_ACCOUNT = os.environ["Twitter_ACCOUNT"]


# GitHubおよびtwiterのURL
url_userpage = "https://github.com/" + GitHub_ACCOUNT
url_get_name = "https://api.twitter.com/1.1/users/show.json?screen_name=" + Twitter_ACCOUNT
url_post_name = "https://api.twitter.com/1.1/account/update_profile.json"


# タイムゾーンを設定
TIMEZONE = "Asia/Tokyo"
jst = pytz.timezone(TIMEZONE)
today_date = datetime.now(jst).strftime("%Y-%m-%d")


# 進捗状況一覧
words_dict = {
    "#ebedf0": "進捗ない", 
    "#c6e48b": "ちょっと頑張っている", 
    "#7bc96f": "まあまあ頑張っている", 
    "#239a3b": "結構頑張っている", 
    "#196127": "かなり頑張っている"
    }


# 今日のcontributionを取得し、カラーコードから進捗状況を作成
cookie = {"tz": TIMEZONE}
res_g = requests.get(url_userpage, cookies=cookie)
soup = BeautifulSoup(res_g.text)
today_contribution = soup.find("rect", {"data-date": today_date}) 
statement = "@今日は" + words_dict[today_contribution['fill']] + "みたい"


# twitterの名前の@以下を書き換える
twitter = OAuth1Session(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET)
res_t = twitter.get(url_get_name)
new_name = res_t.json()["name"].split("@")[0] + statement
param = {"name": new_name}
r = twitter.post(url_post_name, param)
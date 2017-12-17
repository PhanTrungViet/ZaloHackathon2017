
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, request
import telepot
import urllib3


import re
patterns = {
    '[àáảãạăắằẵặẳâầấậẫẩ]': 'a',
    '[đ]': 'd',
    '[èéẻẽẹêềếểễệ]': 'e',
    '[ìíỉĩị]': 'i',
    '[òóỏõọôồốổỗộơờớởỡợ]': 'o',
    '[ùúủũụưừứửữự]': 'u',
    '[ỳýỷỹỵ]': 'y'
}

import pandas as pd
from sklearn.externals import joblib
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
tfidf_transformer = TfidfTransformer()
vocabulary = joblib.load('/home/quangtien/mysite/name_vect.pkl')
count_vect = CountVectorizer(binary=True, vocabulary = vocabulary)
clf = joblib.load('/home/quangtien/mysite/name_model.pkl')

proxy_url = "http://proxy.server:3128"
telepot.api._pools = {
    'default': urllib3.ProxyManager(proxy_url=proxy_url, num_pools=3, maxsize=10, retries=False, timeout=30),
}
telepot.api._onetime_pool_spec = (urllib3.ProxyManager, dict(proxy_url=proxy_url, num_pools=1, maxsize=1, retries=False, timeout=30))

secret = "c5d3ccd5-5c31-4d35-a066-e34c185c449f"
bot = telepot.Bot('487232634:AAEOkcjblcggtL5eOa-6wJTwjQjFmULc9Kw')
bot.setWebhook("https://quangtien.pythonanywhere.com/{}".format(secret), max_connections=1)

app = Flask(__name__)

@app.route('/{}'.format(secret), methods=["POST"])
def telegram_webhook():
    update = request.get_json()
    if "message" in update:
        text = update["message"]["text"]
        chat_id = update["message"]["chat"]["id"]

        if text == "/start":
            bot.sendMessage(chat_id, "Chào bạn!")
            return "OK"

        if text == "vng":
            bot.sendLocation(chat_id, 10.764328, 106.656222)
            return "OK"

        for regex, replace in patterns.items():
            text = re.sub(regex, replace, text)

        test = pd.Series(text)
        test = count_vect.transform(test)
        test_tfidf = tfidf_transformer.fit_transform(test)
        results = clf.predict(test_tfidf)


        r = results[0]
        df = pd.read_excel('/home/scivihackathon/mysite/fpt.xlsx')
        reps = df.loc[df['name'] == r]['nameUrl']
        for rep in reps:
        bot.sendMessage(chat_id,name + r)

    return "OK"
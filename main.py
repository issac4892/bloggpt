import os
import requests
import threading
from notionai import NotionAI
from dotenv import load_dotenv
from datetime import datetime
from urllib.parse import urljoin
import json


load_dotenv()
TOKEN = os.environ.get("NOTION_TOKEN")
WP_URL = 'https://testbed.algorix.io'
WP_USERNAME = 'algorix'
WP_PASSWORD = os.environ.get("PW")
status = 'publish'
slug = 'posts'
category_ids = [1]

def process():
    ai = NotionAI(TOKEN)
    topic = ai.blog_post(
        "I want you to write out one small but important development common sense topic in Korean in the form of an interrogative sentence. I want a different topic than the ones you've answered before. Only write the first line and never add any additional explanation after it. Don't put any symbols in the sentences, just text. Don't put spaces at the beginning and end of the sentences. Do not put a space at the beginning of a sentence.")
    print(f'토픽 생성 완료: {topic}')

    article = ai.blog_post(
        f"Write a very long technical article about {topic} in English. When you end your reply, do so naturally, bringing everything to a close. Don't cut off sentences mid-sentence, but finish them. Write at least 50 lines of text. Don't write in markdown, just plain text that will go into a blog post.")
    print(f'아티클 생성 완료: {article}')

    payload = {
        "status": status,
        "slug": slug,
        "title": topic,
        "content": article,
        "date": datetime.now.isoformat(),
        "categories": category_ids
    }

    res = requests.post(urljoin(WP_URL, "wp-json/wp/v2/posts"),
        data=json.dumps(payload),
        headers = {'Content-type': "application/json"},
        auth=(WP_USERNAME, WP_PASSWORD)
    )

    if res.ok :
        print(f"{res.status.code}")
    else:
        print(f"error {res.status.code}")

    threading.Timer(3600, process).start()


if __name__ == '__main__':
    process()

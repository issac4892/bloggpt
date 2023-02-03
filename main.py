import os
import requests
import threading
from notionai import NotionAI
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.environ.get("NOTION_TOKEN")
TISTORY_ACCESS_TOKEN = os.environ.get("TISTORY_ACCESS_TOKEN")


def process():
    ai = NotionAI(TOKEN)
    topic = ai.blog_post(
        "소소하면서 중요한 개발 상식 주제 1가지를 의문문 문장 형태로 한국어로 출력해줘. 이전에 대답한 주제들과는 다른 주제를 원해. 오직 처음 한 줄로 충력하고 절대로 그 뒤에 아무런 부가 설명도 붙이지 마. 문장에 어떤 기호도 붙이지 말고 텍스트만 출력해. 문장 처음과 끝에 공백을 넣지 마십시오. 문장 가장 처음에 공백을 넣지 마십시오.")
    print(f'토픽 생성 완료: {topic}')

    article = ai.blog_post(
        f"'{topic}'에 대한 기술 관련 글을 한국어로 매우 길게 작성하세요. 답장을 끝낼때는 모든 상황을 마무리 지으면서 자연스럽게 끝내십시오. 문장을 중간에 끊지 말고 끝까지 이으세요. 적어도 50줄 이상의 글을 작성하세요. 마크다운 식으로 작성하지 말고, 블로그 글에 들어갈 일반 텍스트들로만 작성하세요.")
    print(f'아티클 생성 완료: {article}')

    tags = ai.blog_post(
        f"'{topic}'에 대한 적절한 태그를 10개 이상 50개 이하로 작성해주세요. ','로 구분합니다. 한글로 작성하고 한 태그는 하나의 단어로 이루어져 있습니다. '#'을 사용하지 않고 단어만 작성하십시오. ',' 뒤에 공백을 넣지 말고 다음 태그와 붙여서 쓰십시오.")
    print(f'태그 생성 완료: {tags}')

    requests.post(
        f"https://www.tistory.com/apis/post/write?access_token={TISTORY_ACCESS_TOKEN}&blogName=daily-dev-knowledge&title={topic}&visibility=3&content={article}&tag={tags}")
    print('아티클 업로드 완료!')

    threading.Timer(3600, process).start()


if __name__ == '__main__':
    process()

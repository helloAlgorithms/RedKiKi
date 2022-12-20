from slack_sdk import WebClient
import os
from dotenv import load_dotenv

class SlackAPI:
    """
    슬랙 API 핸들러
    """
    def __init__(self, token):
        # 슬랙 클라이언트 인스턴스 생성
        self.client = WebClient(token)
        
    def get_channel_id(self, channel_name):
        """
        슬랙 채널ID 조회
        """
        # conversations_list() 메서드 호출
        result = self.client.conversations_list()
        # 채널 정보 딕셔너리 리스트
        channels = result.data['channels']
        # 채널 명이 'test'인 채널 딕셔너리 쿼리
        channel = list(filter(lambda c: c["name"] == channel_name, channels))[0]
        # 채널ID 파싱
        channel_id = channel["id"]
        return channel_id

    def post_thread(self, channel_id, text):
        """
        슬랙 채널 내 메세지의 Thread에 댓글 달기
        """
        # chat_postMessage() 메서드 호출
        result = self.client.chat_postMessage(
            channel=channel_id,
            text = text,
        )
        return result

load_dotenv()
token = os.environ.get("SLACK_BOT_USER_OAUTH_TOKEN")
slack = SlackAPI(token)

channel_name = "vacation-notice"
query = "슬랙 봇 테스트"
text = "자동 생성 문구 테스트"

# 채널ID 파싱
channel_id = slack.get_channel_id(channel_name)
#os.system("rm -rf helloAlgorithms")
os.system("git clone https://github.com/helloAlgorithms/helloAlgorithms.git")
print("============================")
raw_list = list(map(str, os.popen("cd helloAlgorithms && git branch -r")))
user_list = []
for raw in raw_list[1::]:
     user = raw.strip().split('/')[1]
     user_list.append(user)
print(user_list)
print("============================")
commit_count = os.popen("cd helloAlgorithms \
        && git checkout {user} && \
           git log --since=2.weeks --pretty=format:{git_log_format} \
           --grep {bracket} | sort -k 3 | wc -l".format(user = user_list[0], git_log_format = '"%cr : %s"',bracket=r'['))
print(*commit_count)
slack.post_thread(channel_id, text)

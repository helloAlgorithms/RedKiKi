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

channel_id = slack.get_channel_id(channel_name)
os.system("git clone https://github.com/helloAlgorithms/helloAlgorithms.git")
raw_list = list(map(str, os.popen("cd helloAlgorithms && git branch -r")))
users = []
for raw in raw_list[1::]:
     user = raw.strip().split('/')[1]
     users.append(user)
users.remove("master")
users.remove("test")

vacation_users = {}
pass_users = {}
for user in users:
    os.system("cd helloAlgorithms && git checkout {user}".format(user = user))
    raw_commit_count = os.popen("cd helloAlgorithms && \
            git log --since=2.weeks --pretty=format:{git_log_format} \
            --grep {bracket} | sort -k 3 | wc -l".format(user = user, git_log_format = '"%cr : %s"',bracket='"\["'))
    commit_count = raw_commit_count.read()
    commit_count.strip()
    commit_count = int(commit_count)
    if commit_count < 8:
        vacation_users[user] = commit_count
    else:
        pass_users[user] = commit_count

vacation_users = sorted(vacation_users.items(), key = lambda x:x[1])
pass_users = sorted(pass_users.items(), key = lambda x:x[1], reverse = True)

vacation_text = ":cry: vacation members :cry:\n"
pass_text = ":laughing: passed members :laughing:\n"

for index, user in enumerate(vacation_users):
    text = f":desert_island:`{user[0]}`"
    width = 11 - len(user[0])
    text +=  " " * width
    text += f"{user[1]}\t"
    if (index + 1) % 4 == 0:
        text += "\n"
    vacation_text += text 
if len(vacation_users) == 0:
    vacation_text += "No one goes to vacation!!:partying_face:\n"

for index, user in enumerate(pass_users):
    text = f":fire:`{user[0]}`"
    width = 11 - len(user[0])
    text +=  " " * width
    text += f"{user[1]}\t"
    if (index + 1) % 4 == 0:
        text += "\n"
    pass_text += text
if len(pass_users) == 0:
    pass_text += "Doomsday :skull_and_crossbones:\n"

slack.post_thread(channel_id, vacation_text)
slack.post_thread(channel_id, pass_text)

os.system("rm -rf helloAlgorithms")

import os
from datetime import datetime
import slack_api
from dotenv import load_dotenv


def get_post_text(users, origin_text, defalut_text, emoji):
	ret_text = origin_text;
	for index, user in enumerate(users):
		text = f"{emoji}`{user[0]}`"
		width = 11 - len(user[0])
		text +=  " " * width
		text += f"{user[1]}\t"
		if (index + 1) % 4 == 0:
			text += "\n"
		ret_text += text 
		if len(users) == 0:
			ret_text += defalut_text
	return ret_text

def run_vactino_checker():
	load_dotenv()
	# action per 2 weeks.
	if datetime.now().isocalendar()[1] % 2 == 0:
		exit(0)

	token = os.environ.get("SLACK_BOT_USER_OAUTH_TOKEN")
	slack = slack_api.slack_api(token)
	channel_name = os.environ.get("VACATION_NOTICE_CHANNEL_NAME")
	channel_id = slack.get_channel_id(channel_name)
	repo_url = os.environ.get("REPO_URL")
	repo_name = os.environ.get("REPO_NAME")
	os.system("git clone " + repo_url)
	raw_list = list(map(str, os.popen(f"cd {repo_name} && git branch -r")))
	users = []
	for raw in raw_list[1::]:
		user = raw.strip().split('/')[1]
		users.append(user)
	users.remove("master")
	users.remove("test")

	vacation_users = {}
	pass_users = {}
	for user in users:
		os.system("cd {repo_name} && git checkout {user}".format(repo_name = repo_name, user = user))
		raw_commit_count = os.popen("cd {repo_name} && \
				git log --since=2.weeks --pretty=format:{git_log_format} \
				--grep {bracket} | sort -k 3 | wc -l".format(repo_name = repo_name, user = user, git_log_format = '"%cr : %s"',bracket='"\["'))
		commit_count = raw_commit_count.read()
		commit_count.strip()
		commit_count = int(commit_count)
		if commit_count < 8:
			vacation_users[user] = commit_count
		else:
			pass_users[user] = commit_count

	vacation_users = sorted(vacation_users.items(), key = lambda x:x[1])
	pass_users = sorted(pass_users.items(), key = lambda x:x[1], reverse = True)
	vacation_prefix_text = ":cry: vacation members :cry:\n"
	pass_perfrix_text = ":laughing: passed members :laughing:\n"
	vacation_text = get_post_text(vacation_users, vacation_prefix_text, "No one goes to vacation!!:partying_face:\n", ":desert_island:")
	pass_text = get_post_text(pass_users, pass_perfrix_text, "Doomsday :skull_and_crossbones:\n", ":fire:")

	slack.post_thread(channel_id, vacation_text)
	slack.post_thread(channel_id, pass_text)

	os.system(f"rm -rf {repo_name}")

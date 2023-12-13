import json
import re
import os

# Regex pattern to match double quoted substrings or words
pattern = r'\".*?\"|\S+'

entries = os.listdir('logs')

files = [f for f in entries if os.path.isfile(os.path.join('logs', f))]

# Step 1: Open the file
log_count = 0
user_agent_set = set()

for log_file in files:
    with open(os.path.join('logs', log_file), 'r') as file:
        data = json.load(file)
        for log in data:
            log_count = log_count + 1
            text_payload = log["textPayload"]
            substrings = re.findall(pattern, text_payload)
            user_agent_set.add(substrings[12])

print(f"전체 로그수 : ${log_count}, User-agent 종류 갯수 : ${len(user_agent_set)}")

print(f"Unique user-agent 목록:")
sorted_user_agent = sorted(user_agent_set)
for user_agent in sorted_user_agent:
    print(f"{user_agent}")

import os
from dotenv import load_dotenv
import requests

load_dotenv()
MISSKEY_URL = os.getenv("MISSKEY_URL")
MISSKEY_TOKEN = os.getenv("MISSKEY_TOKEN")

misskey_token_modified = "Bearer " + MISSKEY_TOKEN

user_id = input("ユーザーID: ")

# 実行確認
print("指定したユーザのドライブにある全ファイルが削除されます。")
confirmation = input('非常に危険な操作です！実行する場合は"yes"と入力してください: ')
if confirmation != "yes":
    print("実行を中止しました")
    exit(0)

res = requests.post(
    f"{MISSKEY_URL}/api/admin/delete-all-files-of-a-user",
    headers={
        "Authorization": misskey_token_modified,
        "Content-Type": "application/json",
    },
    json={"userId": user_id},
)

if res.status_code != 204:
    print(f"Error: {res.status_code}: {res.json()['error']['message']}")
    exit(1)

print("削除が完了しました")

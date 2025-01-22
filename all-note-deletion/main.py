import os
import time
from dotenv import load_dotenv
import requests

load_dotenv()
MISSKEY_URL = os.getenv("MISSKEY_URL")
MISSKEY_TOKEN = os.getenv("MISSKEY_TOKEN")

misskey_token_modified = "Bearer " + MISSKEY_TOKEN

# userIdを取得
try:
    res = requests.post(
        f"{MISSKEY_URL}/api/i",
        headers={
            "Authorization": misskey_token_modified,
            "Content-Type": "application/json",
        },
        json={},
    )
except Exception as e:
    print(f"Error: {e}")
    exit(1)

if res.status_code != 200:
    print(f"Error: {res.status_code}: {res.json()['error']['message']}")
    exit(1)

user_id = res.json()["id"]

while True:
    # ノートを取得
    try:
        res = requests.post(
            f"{MISSKEY_URL}/api/users/notes",
            headers={
                "Authorization": MISSKEY_TOKEN,
                "Content-Type": "application/json",
            },
            json={
                "userId": user_id,
                "limit": 100,
                "withReplies": True,
                "withChannelNotes": True,
            },
        )
    except Exception as e:
        print(f"Error: {e}")
        exit(1)

    if res.status_code != 200:
        print(f"Error: {res.status_code}: {res.json()['error']['message']}")
        exit(1)

    notes = res.json()

    if len(notes) == 0:
        print("No notes found. Exiting...")
        break

    for note in notes:
        # ノートを削除
        try:
            res = requests.post(
                f"{MISSKEY_URL}/api/notes/delete",
                headers={
                    "Authorization": misskey_token_modified,
                    "Content-Type": "application/json",
                },
                json={"noteId": note["id"]},
            )
        except Exception as e:
            print(f"Error: {e}")
            exit(1)

        if res.status_code != 204:
            print(f"Error: {res.status_code}: {res.json()['error']['message']}")
            exit(1)

        print(f"Deleted: {note['id']}")

        # レートリミット回避
        time.sleep(1)

import argparse
import json
import os
import readline
import zipfile

from tqdm import tqdm

# 引数設定
arg_parser = argparse.ArgumentParser(
    prog="Misskey emoji compress",
    usage="python main.py -d <dir>",
    description="Misskeyの絵文字インポート用zipファイルを生成します。",
    add_help=True,
)
arg_parser.add_argument(
    "-d", "--dir", help="画像ファイルが入っているディレクトリ", required=True
)
args = arg_parser.parse_args()

# ディレクトリ存在確認
if not os.path.isdir(args.dir):
    print(f"Error: ディレクトリ{args.dir}が不正です")
    exit(1)

category = input("カテゴリ: ")
license_text = input("ライセンス: ")
isSensitive = input("センシティブ(y/n, デフォルト: n): ") == "y"
isLocal = input("ローカルのみ(y/n, デフォルト: n): ") == "y"

print('Tips: "-"は"_"に置換されます')

json_data = {"emojis": []}

for file_name in tqdm(os.listdir(args.dir), desc="処理中"):
    # .DS_Storeファイルはスキップ
    if os.path.basename(file_name) == ".DS_Store":
        continue

    emoji = {
        "downloaded": True,
        "fileName": os.path.basename(file_name).replace("-", "_").replace(" ", "_"),
        "emoji": {
            "name": os.path.splitext(os.path.basename(file_name))[0]
            .replace("-", "_")
            .replace(" ", "_"),
            "category": category,
            "license": license_text,
            "localOnly": isLocal,
            "isSensitive": isSensitive,
        },
    }

    json_data["emojis"].append(emoji)

# ファイル書き込み
with zipfile.ZipFile("emojis.zip", "w") as zip_file:
    for file_name in os.listdir(args.dir):
        # .DS_Storeファイルはスキップ
        if os.path.basename(file_name) == ".DS_Store":
            continue

        zip_file.write(
            os.path.join(args.dir, file_name),
            file_name.replace("-", "_").replace(" ", "_"),
        )

    with zip_file.open("meta.json", "w") as meta_json:
        meta_json.write(
            json.dumps(json_data, indent=2, ensure_ascii=False).encode("utf-8")
        )

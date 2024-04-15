
import datetime
from src.Client import Client
from src.Bot import Bot
import time


model_id = "kanhatakeyama/0405_100m_clean_ja"
model_id = "mistral-community/Mixtral-8x22B-v0.1"
model_id = "llm-jp/llm-jp-13b-dpo-lora-hh_rlhf_ja-v1.1"
peft_path = "/home/hatakeyama/python/mixtral/outputs/mixtral_1kdolly_1epoch"
peft_path = ""

with open("env/url.txt") as f:
    url = f.read().strip()

# クライアント
client = Client(url)

# モデル

bot = Bot(model_id, peft_path=peft_path)

while True:
    # 未回答の質問を取得
    while True:
        try:
            row_id, question, inst = client.get_unanswered_question()
            if question == "":
                print("no question to answer")
                break

            prompt = inst+"\n###入力:\n"+question+"\n###応答:\n"
            print(prompt)

            # 回答させる
            response = bot.ask(question)

            # 回答を送信
            client.answer(row_id, response, model_id +
                          "time:"+datetime.datetime.now().isoformat())
        except Exception as e:
            print(e)
            time.sleep(5)
            continue
    time.sleep(60)

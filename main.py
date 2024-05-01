
import datetime
from src.Client import Client
# from src.Bot import Bot
# from src.MixtralBot import MixtralBot
import random
from src.GGUFBot import GGUFBot
import time


peft_path = ""
model_id = "kanhatakeyama/0405_100m_clean_ja"
model_id = "mistral-community/Mixtral-8x22B-v0.1"
model_id = "mistralai/Mixtral-8x22B-Instruct-v0.1"
# model_id = "llm-jp/llm-jp-13b-dpo-lora-hh_rlhf_ja-v1.1"
# peft_path = "/home/hatakeyama/python/ChatServer/outputs/mixtral_1epoch_0415"

with open("env/url.txt") as f:
    url = f.read().strip()

# apiクライアントとchatbotを起動
client = Client(url)

# bot = Bot(model_id, peft_path=peft_path)
# bot=MixtralBot(model_id, peft_path=peft_path)
bot = GGUFBot(
    model_path="/data/2023/1505llmmatsu/mixtral_gguf/model/Mixtral-8x22B-Instruct-v0.1.Q5_K_M-00001-of-00004.gguf")
mixtral_mode = True


def generate_prompt(inst_template, question):
    inst1, inst2 = inst_template.split("{question}")
    inst2 = inst2.replace("{answer}", "")
    return inst1+question+inst2


count = 0
no_question_count = 0
while True:
    # 未回答の質問を取得
    while True:
        if client.current_sheet_id == 1:
            count += 1
            if count > 2:
                count = 0
                client.set_sheet_id(0)
        try:
            print("fetching questions")
            row_id, question, inst = client.get_unanswered_question()
            print((question))

            # 何も質問がない状態が続いた場合､自分で質問を作る
            if no_question_count > 5 and question == "":
                client.set_sheet_id(0)
                client.get_q_and_a()
                # row_id, question, inst = client.get_unanswered_question()
                row_id = len(client.questions)+1
                print("last question: "+client.questions[-1])
                print(f"generating new questions. row_id: {row_id}")
                question = random.choice(client.questions)
                prompt = f"""以下の問題・質問・指示の類題を日本語で作成してください。
・類題はもとの問題からは必ず情報を追加・修正・削除し、内容、形式、記述方式が全く異なるようにすること
・作成した内容のみを出力し､回答は絶対に出力しないこと
{question}
類題: 
"""

                print("prompt", prompt)
                client.sheet.update(
                    f'A{row_id}', [["automatically generating a question..."]])
                question = bot.ask(prompt)
                if question == "":
                    continue
                print("new question", question)
                client.sheet.update(f'A{row_id}', [[question]])
                no_question_count = 0
                count = 0
                continue
            if question == "":
                print("no question to answer")
                no_question_count += 1
                if client.current_sheet_id == 0:
                    client.set_sheet_id(1)
                else:
                    client.set_sheet_id(0)
                break

            # 回答させる
            response1 = bot.ask(question)
            # response2 = bot.ask(question)
            response2 = "-"
            if response1 == "":
                response1 = "-"
            if response2 == "":
                response2 = "-"
            response1 = response1.strip()
            print("response:", response1, response2)
            no_question_count = 0

            # 回答を送信
            client.answer(row_id, response1, response2, model_id +
                          "time:"+datetime.datetime.now().isoformat())
        except Exception as e:
            print(e)
            time.sleep(1)
            continue
    time.sleep(1)

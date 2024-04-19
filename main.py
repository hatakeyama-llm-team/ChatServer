
import datetime
from src.Client import Client
from src.Bot import Bot
from src.MixtralBot import MixtralBot
import time


peft_path = ""
model_id = "kanhatakeyama/0405_100m_clean_ja"
model_id = "mistral-community/Mixtral-8x22B-v0.1"
model_id="mistralai/Mixtral-8x22B-Instruct-v0.1"
#model_id = "llm-jp/llm-jp-13b-dpo-lora-hh_rlhf_ja-v1.1"
#peft_path = "/home/hatakeyama/python/ChatServer/outputs/mixtral_1epoch_0415"

with open("env/url.txt") as f:
    url = f.read().strip()

#apiクライアントとchatbotを起動
client = Client(url)

#bot = Bot(model_id, peft_path=peft_path)
bot=MixtralBot(model_id, peft_path=peft_path)
mixtral_mode=True

def generate_prompt(inst_template, question):
    inst1,inst2=inst_template.split("{question}")
    inst2=inst2.replace("{answer}","")
    return inst1+question+inst2

while True:
    # 未回答の質問を取得
    while True:
        try:
            print("fetching questions")
            row_id, question, inst = client.get_unanswered_question()
            print((question))
            if question == "":
                print("no question to answer")
                break
            
            if mixtral_mode:
                response=bot.ask(question)
            else:
                #prompt = inst+"\n###入力:\n"+question+"\n###応答:\n"
                prompt=generate_prompt(inst,question)
                print(prompt)

                # 回答させる
                response = bot.ask(prompt)
            if response == "":
                response = "-"
            print("response:", response)

            # 回答を送信
            client.answer(row_id, response, model_id +
                          "time:"+datetime.datetime.now().isoformat())
        except Exception as e:
            print(e)
            time.sleep(10)
            continue
    time.sleep(10)

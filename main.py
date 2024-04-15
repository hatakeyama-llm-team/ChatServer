
import datetime
from src.Client import Client
from src.Bot import Bot
import time


model_id="kanhatakeyama/0405_100m_clean_ja"
model_id = "mistral-community/Mixtral-8x22B-v0.1"
with open("env/url.txt") as f:
    url = f.read().strip()

#クライアント
client=Client(url)

#モデル

bot=Bot(model_id)

while True:
    #未回答の質問を取得
    while True:
        try:
            row_id,question,inst=client.get_unanswered_question()
            if question=="":
                print("no question to answer")
                break
                
            prompt=inst+"\nQ."+question+"\nA."
            print(prompt)

            #回答させる
            response=bot.ask(question)

            #回答を送信 
            client.answer(row_id,"model:"+response,model_id+"time:"+datetime.datetime.now().isoformat())
        except Exception as e:
            print(e)
            time.sleep(5)
            continue
    time.sleep(60)
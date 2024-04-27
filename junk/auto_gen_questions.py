# %%
from llama_cpp import Llama
from src.GGUFBot import GGUFBot
import pandas as pd

# %%
df=pd.read_csv('data/original_q copy.csv') # indexはなし
original_question_list=df["question"].values.tolist()
original_question_list

# %%

model_path= "model/Mixtral-8x22B-Instruct-v0.1.Q5_K_M-00001-of-00004.gguf"
bot=GGUFBot(model_path,max_new_tokens=4000,n_ctx=4000,n_gpu_layers=400)

# %%
import json
import random
out_path="data/t1.jsonl"

question=random.choice(original_question_list)
question_template = f"""以下の問題の類題を作成してください。
・類題はもとの問題からは必ず情報を追加・修正・削除し、内容、形式、記述方式が全く異なるようにすること
・問題文のみを出力すること

#問題
"""
while True:
    q=question_template+question
    try:
        new_question=bot.ask(q).replace("#類題","").replace("#問題","").strip()[:3000]
        ans=bot.ask(new_question)
        d={"question":new_question,"answer":ans}
        with open(out_path, 'a') as f:
            f.write(json.dumps(d,ensure_ascii=False)+"\n")
    except:
        pass
    question=new_question
    #question=question[:random.randint(0,len(question))]
    if random.randint(0,3)==0:
        question=question[:int(len(question)*0.8)]
    elif random.randint(0,3)==1:
        question=question[int(len(question)*0.2):]
    if random.randint(0,10)==0:
        question=random.choice(original_question_list)

# %%




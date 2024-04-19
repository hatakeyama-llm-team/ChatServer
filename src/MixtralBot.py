from transformers import AutoModelForCausalLM
from mistral_common.protocol.instruct.messages import (
    AssistantMessage,
    UserMessage,
)
from mistral_common.tokens.tokenizers.mistral import MistralTokenizer
from mistral_common.tokens.instruct.normalize import ChatCompletionRequest
import torch

class MixtralBot:
    def __init__(self,model_id="mistral-community/Mixtral-8x22B-v0.1",
                peft_path=None,
                 max_new_tokens=1000) -> None:
        print("loading model...")

        self.model = AutoModelForCausalLM.from_pretrained(model_id,device_map="auto")
        self.tokenizer= MistralTokenizer.v3()
        self.max_new_tokens=max_new_tokens

        if peft_path:
            print("loading adapter")
            self.model.load_adapter(peft_path)

    def ask(self,question):
        device="cuda"
        mistral_query = ChatCompletionRequest(
            messages=[
                UserMessage(content=question),
            ],
            model="test",
        )

        encodeds = self.tokenizer.encode_chat_completion(mistral_query).tokens
        encodeds = torch.tensor(encodeds).unsqueeze(0) 
        model_inputs = encodeds.to(device)
        generated_ids = self.model.generate(model_inputs, max_new_tokens=self.max_new_tokens, do_sample=True)
        sp_tokenizer = self.tokenizer.instruct_tokenizer.tokenizer
        decoded = sp_tokenizer.decode(generated_ids.tolist())
        return decoded[0][len(question):]
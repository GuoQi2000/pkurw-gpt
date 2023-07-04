import openai
import time

SYSTEM_PROMPT = {"SNLI":"You are a expert at natrual language inference. You will be asked the relationship of a Premise and Hypothesis. You \
         answer can be one of the three: 'neutral','etailment' and 'contradiction'."
                 }

class GPT():
    def __init__(self) -> None:
        openai.api_key = "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"
        self.MODEL = "gpt-3.5-turbo-0613"

    def verbalize(self,content,task):
        if task == "SNLI":
            return content.split(" ")[-1][:-1]
        else:
            pass

    def response(self, prompt,task):
        res = openai.ChatCompletion.create(
        model=self.MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT[task]},
            {"role": "user", "content": prompt}
        ],
        temperature=0,
        )
        content = res['choices'][0]['message']['content']
        answer = self.verbalize(content,task)
        return answer

    def run(self,task,prompt_pool, result_pool,flag):
        print('init gpt')
        while flag:
            if len(prompt_pool) > 0:
                prompt = prompt_pool.pop(0)
                answer = self.response(prompt, task)
                result_pool.append(answer)
                print("predict: ", prompt, " ", answer)
                time.sleep(21)
    
import openai
import time

SYSTEM_PROMPT = {"SNLI":"You are a expert at natrual language inference. You will be asked the relationship of a Premise and Hypothesis. Your \
         answer can be one of the three: 'neutral','etailment' and 'contradiction'.",
         "FEVER":"You are a expert at  fact verification . You will be asked whether a Claim is valid in the context of a Evidence. Your \
         answer can be one of the three: 'support','refute' and 'not enough information'.",
         "QQP":"You are a expert at analyzing the semantics of questions. You will be asked whether The two questions are semantically equivalent. Your \
         answer can be one of the two: 'equivalent' and 'not equivalent'."
                 }

class GPT():
    def __init__(self,key) -> None:
        openai.api_key = key
        self.MODEL = "gpt-3.5-turbo-0613"

    def verbalize(self,content,task):
        if task == "SNLI":
            for label in ["neutral","entailment","contradiction"]:
                if label in content:
                    return label
        elif task == "FEVER":
            for label in ["support","refute","not enough information"]:
                if label in content:
                    return label
        elif task == "QQP":
            for label in ["not equivalent","equivalent"]:
                if label in content:
                    return label

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
        print(content)
        answer = self.verbalize(content,task)
        return answer

    def run(self,submit,request,flag):
        print('init gpt')
        while flag:
            prompt_tuple = request()
            if not prompt_tuple is None:
                prompt = prompt_tuple['prompt']
                user_id = prompt_tuple['user_id']
                task = prompt_tuple['task']
                answer = self.response(prompt, task)
                submit( {'result':answer,'user_id':user_id,'task':task,'time':time.time()} )
                print("predict: ", prompt, " ", answer)
                time.sleep(21)
    
import openai
import time
import logging

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

    def exception_process(self,exception):
        logging.error(exception)

    def response(self, prompt,task):
        try:
            res = openai.ChatCompletion.create(
            model=self.MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT[task]},
                {"role": "user", "content": prompt}
            ],
            temperature=0,
            )
            content = res['choices'][0]['message']['content']
       #     print(content)
            answer = self.verbalize(content,task)
            return answer
        except Exception as e:
            self.exception_process(e)
            return None
        # except openai.error.RateLimitError:
        #     print('rate limit')
        #     print('1. Send fewer tokens or requests or slow down your usage.')
        #     print('2. Wait until your rate limit resets (one minute) and retry your request.')
        #     print('3. Check your API usage statistics from your account dashboard.')
        #     return None
        # except openai.error.ServiceUnavailableError:
        #     print('service unavailable')
        #     print('1. Wait a few minutes and retry your request.')
        #     print("2. Check OpenAI's status page for any ongoing incidents or maintenance.")
        #     return None
        # except openai.error.APIError:
        #     print('APIError encountered, please:')
        #     print('1. Wait a few seconds and retry your request.')
        #     print('2.Wait a few seconds and retry your request.')
        #     return None
        # except openai.error.Timeout:
        #     print('Timeout encountered, please:')
        #     print('1. Wait a few seconds and retry your request.')
        #     print('2. Check your network settings and ensure you have a stable and fast internet connection.')
        #     return None
        # except openai.error.APIConnectionError:
        #     print('APIConnectionError encountered, please:')
        #     print('1. Check your proxy configuration, SSL certificates, and firewall rules.')
        #     print('2. Check your network settings and ensure you have a stable and fast internet connection.')
        #     return None
        # except openai.error.AuthenticationError:
        #     print('AuthenticationError encountered, please:')
        #     print('1. Check your API key or token and ensure it is correct and active.')
        #     print('2. Ensure you have followed the correct formatting.')
        #     return None

    def run(self,submit,request,flag):
        logging.info('init gpt')
        while flag:
            prompt_tuple = request()
            if not prompt_tuple is None:
                prompt = prompt_tuple['prompt']
                user_id = prompt_tuple['user_id']
                task = prompt_tuple['task']
                answer = self.response(prompt, task)
                if not (answer is None):
                    submit( {'result':answer,'user_id':user_id,'task':task,'time':time.time()} )
                    time.sleep(20)
    
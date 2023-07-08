import openai
import time
import logging

'''
GPT API调用时的system prompt,根据每个任务单独设计.
'''
SYSTEM_PROMPT = {"SNLI":"You are a expert at natrual language inference. You will be asked the relationship of a Premise and Hypothesis. Your \
         answer can be one of the three: 'neutral','etailment' and 'contradiction'.",
         "FEVER":"You are a expert at  fact verification . You will be asked whether a Claim is valid in the context of a Evidence. Your \
         answer can be one of the three: 'support','refute' and 'not enough information'.",
         "QQP":"You are a expert at analyzing the semantics of questions. You will be asked whether The two questions are semantically equivalent. Your \
         answer can be one of the two: 'equivalent' and 'not equivalent'.",
         "CoLA":"You are a expert at grammar. You will be asked whether a sentence has valid grammar. Your \
         answer can be one of the two: 'correct' and 'incorrect'."
                 }

LABEL_MAP = {'SNLI':{"neutral":"neutral","entailment":"entailment","contradiction":"contradiction"},
             'FEVER':{"support":"SUPPORTS","refute":"REFUTES","not enough information":"NOT ENOUGH INFORMATION"},
             'QQP':{"not equivalent":"non-entailment","equivalent":"entailment"},
             'CoLA':{"incorrect":"incorrect","correct":"correct"}}

class GPT():
    '''
    负责直接对openai API的调用
    '''
    def __init__(self,key) -> None:
        openai.api_key = key
        self.MODEL = "gpt-3.5-turbo-0613"

    def verbalize(self,content,task):
        '''
        将gpt的结果转化成标签
        '''
        res_index = content.lower().find("the answer is")
        if res_index >= 0:
            res_content = content[res_index:]
        else:
            res_content = content
        if task == "SNLI":
            for label in ["neutral","entailment","contradiction"]:
                if label in res_content.lower():
                    return LABEL_MAP[task][label]
        elif task == "FEVER":
            for label in ["support","refute","not enough information"]:
                if label in res_content.lower():
                    return LABEL_MAP[task][label]
        elif task == "QQP":
            for label in ["not equivalent","equivalent"]:
                if label in res_content.lower():
                    return LABEL_MAP[task][label]
        elif task == "CoLA":
            for label in ["incorrect","correct"]:
                if label in res_content.lower():
                    return LABEL_MAP[task][label]

    def exception_process(self,exception):
        '''
        简单的异常处理,打印error信息
        返回None代表这次请求失败
        '''
        logging.error(exception)
        return None

    def response(self, prompt,task):
        '''
        openai 的 API调用请求,如果出现调用异常就转入异常处理
        '''
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
            logging.info(f"response : {content}")
            answer = self.verbalize(content,task)
            return answer
        except Exception as e:
            return self.exception_process(e)

    def run(self,submit,request,end):
        '''
        主程序
        不断发生prompt请求,每次得到一个prompt并进行API调用,将结果转化为标签后返回
        每次API调用成功后sleep 20s (调用上限为1分钟3次)
        直到所有任务结束(end==True)
        '''
        logging.info('init gpt')
        while not end:
            prompt_tuple = request()
            if not prompt_tuple is None:
                prompt = prompt_tuple['prompt']
                user_id = prompt_tuple['user_id']
                task = prompt_tuple['task']
                answer = self.response(prompt, task)
                if not (answer is None):
                    submit( {'result':answer,'user_id':user_id,'task':task,'time':time.time()} )
                time.sleep(20)
    
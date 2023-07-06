import time
import logging


'''
TEMPLATE 储存不同人物的prompt模板
'''
TEMPLATE = {"SNLI": "[x] Overall, the relationship between premise and hypothesis is [z].",
            "FEVER": "[x] Overall, considering the Claim only in the context of the Evidence, the answer is [z].",
            "QQP": "[x] Overall, the semantic relationship between the two questions is [z].",
            "CoLA": "[x] Overall, the given sentence is grammatically [z].",
            }

class Processor():
    '''
    processor负责架构中的输入处理,将用户的输入转换成gpt的prompt.
    '''
    def __init__(self):
        pass

    def process(self, task,input_sentence):
        '''
        对输入句子进行处理,得到gpt的prompt
        '''
        if task == "SNLI":
            x = "Premise: "+input_sentence[0]+" Hypothesis: "+input_sentence[1]
        elif task == "FEVER":
            x = "Evidence: "+input_sentence[0]+" Claim: "+input_sentence[1]
        elif task == "QQP":
            x = "Question 1: "+input_sentence[0]+" Question 2: "+input_sentence[1]
        elif task == "CoLA":
            x = "Sentence: "+input_sentence
        prompt = TEMPLATE[task].replace("[x]",x)
        return prompt
    
    def run(self, submit, request, end):
        '''
        processor的主程序
        不断发送input请求,每次得到一个input,将其处理为prompt并提交
        如果请求失败则暂时sleep (processor处理的速度很快,因此一次处理尽可能多的input)
        直到任务结束(end==True)
        '''
        logging.info('init processor')
        while not end:
            prompt_tuple = request()
            if not (prompt_tuple is None):
                input_sentence = prompt_tuple['input_sentence']
                user_id = prompt_tuple['user_id']
                task = prompt_tuple['task']
                prompt = self.process(task, input_sentence)
                submit({'prompt':prompt,'user_id':user_id,'task':task,'time':time.time()})
            else:
                time.sleep(1)

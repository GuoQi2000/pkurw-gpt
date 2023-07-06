import time
import logging

TEMPLATE = {"SNLI": "[x] Overall, the relationship between premise and hypothesis is [z].",
            "FEVER": "[x] Overall, considering the Claim only in the context of the Evidence, the answer is [z].",
            "QQP": "[x] Overall, the semantic relationship between the two questions is [z].",
            }

class Processor():
    def __init__(self) -> None:
        pass

    def process(self, task,input_sentence):
        if task == "SNLI":
            x = "Premise: "+input_sentence[0]+" Hypothesis: "+input_sentence[1]
        elif task == "FEVER":
            x = "Evidence: "+input_sentence[0]+" Claim: "+input_sentence[1]
        elif task == "QQP":
            x = "Question 1: "+input_sentence[0]+" Question 2: "+input_sentence[1]
        prompt = TEMPLATE[task].replace("[x]",x)
        return prompt
    
    def run(self, submit, request, flag):
        logging.info('init processor')
        while flag:
            prompt_tuple = request()
            if not (prompt_tuple is None):
             #   print("process : ",prompt_tuple)
                input_sentence = prompt_tuple['input_sentence']
                user_id = prompt_tuple['user_id']
                task = prompt_tuple['task']
                prompt = self.process(task, input_sentence)
                submit({'prompt':prompt,'user_id':user_id,'task':task,'time':time.time()})
            else:
                time.sleep(1)

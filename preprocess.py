import time


TEMPLATE = {"SNLI": "[x] Overall, the relationship between premise and hypothesis is [z].",

            }

class Processor():
    def __init__(self) -> None:
        pass

    def process(self, task,input_sentence):
        if task == "SNLI":
            x = "Premise: "+input_sentence[0]+" Hypothesis: "+input_sentence[1]
        prompt = TEMPLATE[task].replace("[x]",x)
        return prompt
    
    def run(self,task,input_pool,prompt_pool,flag):
        print('init processor')
        while flag:
            if len(input_pool) > 0:
                input_sentence = input_pool.pop(0)   
                prompt = self.process(task, input_sentence)
                prompt_pool.append(prompt)
            #    print("process")
            else:
                time.sleep(1)

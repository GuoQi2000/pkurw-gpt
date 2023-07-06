import time
import logging

class Manager():
    def __init__(self) -> None:
        self.inputs_pool = []
        self.prompts_pool = []
        self.results_pool = []
        self.temp_prompt_tuple = None
    
    def submit_input(self,input_tuple): # input_tuple = (input_sentence, user_id, task, time)
        t = input_tuple['time']
        for index in range(len(self.inputs_pool)):
            if t < self.inputs_pool[index]['time']:
                self.inputs_pool.insert(index, input_tuple)
                return 
        self.inputs_pool.append(input_tuple)

    def request_input(self):
        if len(self.inputs_pool)>0:
            return self.inputs_pool.pop(0)
        else:
            return None

    def submit_prompt(self,prompt_tuple): # prompt_tuple = (prompt, user_id, task, time)
        t = prompt_tuple['time']
        for index in range(len(self.prompts_pool)):
            if t < self.prompts_pool[index]['time']:
                self.prompts_pool.insert(index, prompt_tuple)
                return
        self.prompts_pool.append(prompt_tuple)

    def request_prompt(self):
        if not (self.temp_prompt_tuple is None):
            return self.temp_prompt_tuple
        if len(self.prompts_pool) > 0:
            prompt_tuple = self.prompts_pool.pop(0)
            self.temp_prompt_tuple = prompt_tuple
            return prompt_tuple
        else:
            return None

    def submit_result(self,result_tuple): # result_tuple = (result, user_id, task, time)
        t = result_tuple['time']
        for index in range(len(self.results_pool)):
            if t < self.results_pool[index]['time']:
                self.results_pool.insert(index,result_tuple)
                return
        self.results_pool.append(result_tuple)
    
    def request_result(self, user_id):
        for result_tuple in self.results_pool:
            if user_id == result_tuple['user_id']:
                self.temp_prompt_tuple = None
                return self.results_pool.pop(0)
        return None

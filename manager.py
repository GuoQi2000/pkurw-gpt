import time
import logging

class Manager():
    '''
        Manager承担整个架构的数据管理
        向user,processor,gpt分别提供接口进行数据读写,保证数据一致性
        并且根据时间对多个user的请求进行调度
    '''
    def __init__(self) -> None:
        '''
        inputs_pool       储存来自各个用户的请求,按照时间先后排列
        prompts_pool      储存processor处理后的prompt,按照时间先后排列
        results_pool      储存gpt给出的结果,按照时间先后排列
        temp_prompt_tuple 储存prompt的临时变量,用于gpt访问失败时重新请求
        '''
        self.inputs_pool = [] 
        self.prompts_pool = [] 
        self.results_pool = []
        self.temp_prompt_tuple = None
    
    def submit_input(self,input_tuple): # input_tuple = (input_sentence, user_id, task, time)
        '''
        input_tuple = (input_sentence, user_id, task, time)
        按照时间顺序插入到inputs_pool当中
        '''
        t = input_tuple['time']
        for index in range(len(self.inputs_pool)):
            if t < self.inputs_pool[index]['time']:
                self.inputs_pool.insert(index, input_tuple)
                return 
        self.inputs_pool.append(input_tuple)

    def request_input(self):
        '''
        processor 请求一个input 进行处理
        优先选择时间最早的input,如果inputs_pool为空则返回None
        '''
        if len(self.inputs_pool)>0:
            return self.inputs_pool.pop(0)
        else:
            return None

    def submit_prompt(self,prompt_tuple):
        '''
        prompt_tuple = (prompt, user_id, task, time)
        按照时间顺序插入到prompts_pool当中
        '''
        t = prompt_tuple['time']
        for index in range(len(self.prompts_pool)):
            if t < self.prompts_pool[index]['time']:
                self.prompts_pool.insert(index, prompt_tuple)
                return
        self.prompts_pool.append(prompt_tuple)

    def request_prompt(self):
        '''
        gpt 请求一个prompt 进行api调用
        优先选择时间最早的prompt,如果prompts_pool为空则返回None
        '''
        if not (self.temp_prompt_tuple is None):
            return self.temp_prompt_tuple
        if len(self.prompts_pool) > 0:
            prompt_tuple = self.prompts_pool.pop(0)
            self.temp_prompt_tuple = prompt_tuple
            return prompt_tuple
        else:
            return None

    def submit_result(self,result_tuple): 
        '''
        result_tuple = (result, user_id, task, time)
        按照时间顺序插入到results_pool当中
        '''
        t = result_tuple['time']
        for index in range(len(self.results_pool)):
            if t < self.results_pool[index]['time']:
                self.results_pool.insert(index,result_tuple)
                return
        self.results_pool.append(result_tuple)
    
    def request_result(self, user_id):
        '''
        user 请求一个result
        优先选择该用户的时间最早的一个result,如果results_pool为空则返回None
        '''
        for result_tuple in self.results_pool:
            if user_id == result_tuple['user_id']:
                self.temp_prompt_tuple = None
                return self.results_pool.pop(0)
        return None

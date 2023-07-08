import openai
import json
import pandas as pd
from torch.utils.data import  Dataset
import time
from User import User
from Processor import Processor
from GPT import GPT
from Manager import Manager
from threading import Thread
import logging

if __name__ == "__main__":
    logging.basicConfig(filename='log.txt',
                     format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s-%(funcName)s',
                     level=logging.INFO)
    api_key = "xxx" 
    # 初始化manager processor gpt实例
    manager = Manager()
    processor = Processor()
    gpt = GPT(api_key)
    # 创建user实例
    user1 = User(1,task='SNLI') 
    user2 = User(2,task='FEVER') 
    user3 = User(3,task='QQP') 
    user4 = User(4,task='CoLA') 
    user1_t = Thread(target=user1.run, args=(manager.submit_input,manager.request_result))
    user2_t = Thread(target=user2.run, args=(manager.submit_input,manager.request_result))
    user3_t = Thread(target=user3.run, args=(manager.submit_input,manager.request_result))
    user4_t = Thread(target=user4.run, args=(manager.submit_input,manager.request_result))
    processor_t = Thread(target=processor.run, args=(manager.submit_prompt,manager.request_input,user1.end&user2.end&user3.end&user4.end))
    gpt_t = Thread(target=gpt.run, args=(manager.submit_result,manager.request_prompt,user1.end&user2.end&user3.end&user4.end))
    
    user1_t.start()
    user2_t.start()
    user3_t.start()
    user4_t.start()
    processor_t.start()
    gpt_t.start()
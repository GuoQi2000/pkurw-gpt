import json
import pandas as pd
from torch.utils.data import  Dataset
import time
import logging


DATA_ROOT = './data/'

PATH_DICT = {
            'SNLI':'SNLI_test.json',
            'FEVER' :'FEVER_symmetric.json',
            'QQP' :'QQP.json',
            'CoLA':'CoLA.json'
            }

def get_path(dataset_name):
    if dataset_name in PATH_DICT.keys():
        return DATA_ROOT + PATH_DICT[dataset_name]
    else:
        print("invalid dataset")

def get_dataset(task):
    if task == "SNLI":
        return SNLIData()
    elif task == "FEVER":
        return FEVERData()
    elif task == "QQP":
        return QQPData()
    elif task == "CoLA":
        return CoLAData()
    else:
        print("invalid dataset")

class SNLIData(Dataset): ## sentence1  sentence2  gold_label
    def __init__(self):
        data = []
        self.data_name = "SNLI"
        path = get_path(self.data_name)
        with open(path, 'r', encoding='utf-8') as f:
            for line in f.readlines():
                data.append(json.loads(line))
        self.df = pd.DataFrame(data)

    def __getitem__(self, index):
        return self.df['sentence1'][index],self.df['sentence2'][index]
    
    def get_label(self,index):
        return self.df['gold_label'][index]
    
    def __len__(self):
        return int(len(self.df))
    
class FEVERData(Dataset): ## sentence1  sentence2  gold_label
    def __init__(self):
        data = []
        self.data_name = "FEVER"
        path = get_path(self.data_name)
        with open(path, 'r', encoding='utf-8') as f:
            for line in f.readlines():
                data.append(json.loads(line))
        self.df = pd.DataFrame(data)

    def __getitem__(self, index):
        return self.df['sentence1'][index],self.df['sentence2'][index]
    
    def get_label(self,index):
        return self.df['gold_label'][index]
    
    def __len__(self):
        return int(len(self.df))
    
class QQPData(Dataset): ## sentence1  sentence2  gold_label
    def __init__(self):
        data = []
        self.data_name = "QQP"
        path = get_path(self.data_name)
        with open(path, 'r', encoding='utf-8') as f:
            for line in f.readlines():
                data.append(json.loads(line))
        self.df = pd.DataFrame(data)

    def __getitem__(self, index):
        return self.df['sentence1'][index],self.df['sentence2'][index]
    
    def get_label(self,index):
        return self.df['gold_label'][index]
    
    def __len__(self):
        return int(len(self.df))

class CoLAData(Dataset): ## sentence1  sentence2  gold_label
    def __init__(self):
        data = []
        self.data_name = "CoLA"
        path = get_path(self.data_name)
        with open(path, 'r', encoding='utf-8') as f:
            for line in f.readlines():
                data.append(json.loads(line))
        self.df = pd.DataFrame(data)

    def __getitem__(self, index):
        return self.df['sentence'][index]
    
    def get_label(self,index):
        return self.df['gold_label'][index]
    
    def __len__(self):
        return int(len(self.df))

class User():
    '''
    一个user实例代表一个用户,支持多个用户的并行访问
    '''
    def __init__(self, id, task):
        '''
        id是区分user的唯一标识符
        task表示用户需要处理的任务
        submit_index指向下一个要处理的数据
        result_pool储存用户得到的返回结果
        end 表示任务是否完成
        '''
        self.id = id
        self.task = task
        self.submit_index = 0
        self.result_pool = []
        self.init_data()
        self.end = False

    def init_data(self):
        '''
        data储存数据集
        true_label是数据集的真实标签
        '''
        self.data = get_dataset(self.task)
        self.true_label = [self.data.get_label(i) for i in range(len(self.data))]
    
    def is_end(self):
        '''
        当结果的数量等于数据集的数量则任务完成
        '''
        return len(self.result_pool) == len(self.data)
    
    def receive(self,answer):
        '''
        将结果添加到result_pool
        '''
        self.result_pool.append(answer)

    def evaluate(self):
        '''
        对分类结果进行测试
        '''
        acc = sum([self.true_label[i]==self.result_pool[i] for i in range(len(self.data))]) / len(self.data) 
        print('user ',self.id,"task ",self.task," finishes, acc = ",acc)
        if self.task == 'QQP' or self.task == 'CoLA':
            if self.task == 'QQP':
                positive_label = 'equivalent'
            else:
                positive_label = 'correct'
            TP = 0
            FP = 0
            FN = 0
            for i in range(len(self.true_label)):
                if self.true_label[i] == self.result_pool[i] and self.true_label == positive_label:
                    TP += 1
                if self.true_label == positive_label and (not self.result_pool[i] == positive_label):
                    FN += 1
                if (not self.true_label == positive_label) and self.result_pool[i] == positive_label:
                    FP += 1
            precision = TP/(TP+FP)
            recall = TP/(TP+FN)
            f1_score = 1 / (1/(precision+1e-5) + 1/(recall+1e-5))
            print('user ',self.id,"task ",self.task," f1_score = ",f1_score)

    def run(self, submit, request):
        '''
        user的主程序
        每隔一段时间发送一次任务请求,每次请求只包含一个数据
        每隔一段时间发送一次结果请求,得到处理结果
        直到任务结束,对最终结果进行评估
        '''
        logging.info(f"init user {self.id} task = {self.task}")
        while not self.end:
            if self.submit_index < len(self.data):
                submit( {'input_sentence':self.data[self.submit_index], 'user_id':self.id,'task':self.task,'time': time.time()} )
                logging.info(f"user {self.id} submits {self.data[self.submit_index]}")
                self.submit_index+=1
            if len(self.result_pool) < len(self.data):
                answer = request(self.id)
                if not (answer is None):
                    self.receive(answer['result'])
                    logging.info(f"user {self.id} receives")
            self.end = self.is_end()
            time.sleep(2)




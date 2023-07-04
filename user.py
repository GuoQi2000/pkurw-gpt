import json
import pandas as pd
from torch.utils.data import  Dataset
import time
import Configure


DATA_ROOT = './data/'

PATH_DICT = {
            'SNLI':'SNLI_test.json',
            'FEVER' :'SNLI/SNLI_train.json',
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
        pass
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

class User():
    def __init__(self, id, task) -> None:
        self.id = id
        self.task = task
        self.emit_index = 0
        self.input_pool = []
        self.prompt_pool = []
        self.result_pool = []
        self.init_data()
        self.flag = True

    def init_data(self):
        self.data = get_dataset(self.task)

    def print_info(self):
        print("User : ",self.id," requests the task : ", self.task, ". Current progress is :", len(self.result_pool)," / ", len(self.data))

    def emit(self):
        res = self.data[self.emit_index]
        self.input_pool.append(res)
        self.emit_index += 1
        return res
    
    def is_end(self):
        return len(self.result_pool) == len(self.data)
    
    def receive(self,answer):
        self.result_pool.append(answer)

    def run(self):
        print('init user')
        while not self.is_end():
            if self.emit_index < len(self.data):
                self.emit()
               # print('emit')
            time.sleep(1)
        self.flag = False



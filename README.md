# 2023北大软微夏令营项目
## update 7.5 
1. 构建了基本框架，划分、实现了user、processor、gpt模块
2. 完成了单线程的文本分类任务
## update 7.6
1. 在原有框架的基础上增加manager模块统一调度多用户的输入输出
2. 完成了多线程多任务的文本分类任务（涵盖SNLI,QQP,FEVER） 
3. todo：GPT调用时的异常处理，断点重连，CoT
## update 7.6(2)
1. 增添了建议的GPT调用异常处理（等待重新请求），实现了简单的断点重爬（API调用失败后重新request），完成了框架。
2. todo：in-context-learning， CoT
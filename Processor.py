import time
import logging


'''
TEMPLATE 储存不同任务的prompt模板
'''
# TEMPLATE = {"SNLI": "Q: [x] Overall, the relationship between premise and hypothesis is [z].",
#             "FEVER": "[x] Overall, considering the Claim only in the context of the Evidence, the answer is [z].",
#             "QQP": "[x] Overall, the semantic re8778777lationship between the two questions is [z].",
#             "CoLA": "[x] Overall, the given sentence is grammatically [z].",
#             }

TEMPLATE = {"SNLI": "Q: [x] Overall, what is the relationship between the premise and the hypothesis? A:",
            "FEVER": "Q: [x] Overall, whether is the claim is valid in the context of the Evidence? A:",
            "QQP": "Q: [x] Overall, what is the semantic relationship between the two questions? A:",
            "CoLA": "Q: [x] Overall, is the given sentence grammatically correct? A:",
            }

SNLI_COT = "Q: Premise: 'Children smiling and waving at camera.' Hypothesis: 'They are smiling at their parents.' What is the relationship between the premise and the hypothesis? A: The premise only states that children are smiling and waving at the camera, but it does not specify who they are smiling at. It is possible that they are smiling at their parents, but it is also possible that they are smiling at something else. Without more information, we cannot conclude whether the hypothesis is true or false. The answer is neutral.\n \
Q: Premise: Two blond women are hugging one another. Hypothesis: There are women showing affection. Overall, what is the relationship between the premise and the hypothesis? A: The premise states that two blond women are hugging each other, providing evidence that supports the hypothesis, as hugging is a form of affection. The answer is entailment\n \
Q: Premise: An older man is drinking orange juice at a restaurant. Hypothesis: Two women are at a restaurant drinking wine. Overall, what is the relationship between the premise and the hypothesis? A: The two statements describe different situations - one with an older man drinking orange juice and the other with two women drinking wine. It is impossible that they are at different positions as the same time. The answer is contradiction\n \
Q: [x] Overall, what is the relationship between the premise and the hypothesis? A: "

FEVER_COT= "Q: Evidence: 'Discovery is an upcoming music album of Lady Gaga .' Claim: 'Discovery is a series .' Overall, whether the evidence supports the claim or refutes it? A: The evidence clearly states that 'Discovery' is an upcoming music album of Lady Gaga, not a series. The answer is refute\n \
                    Q: Evidence: 'Paramore is an American rock band from Franklin , Tennessee , disbanded in 2004 .' Claim: 'In 2004 Paramore collapsed .' Overall, whether the evidence supports the claim or not? A: The evidence states that Paramore disbanded in 2004. Disbanding means that the members of the band decided to end their musical partnership, which can be interpreted as a collapse or dissolution of the band. The answer is support\n \
                    Q: [x] Overall, whether is the claim is valid in the context of the Evidence? A:"

QQP_COT  =  "Q: Question1: 'Which is the best car to buy within 5 lakh range ?' Question2: 'Which is the best car in the range of 3-5 lakhs ?' Overall, what is the semantic relationship between the two questions? A: Although both questions ask about the best car within a specific price range, the first question specifies a range of 5 lakhs, while the second question specifies a range of 3-5 lakhs. This means that the first question is asking for the best car within a fixed price of 5 lakhs, whereas the second question is asking for the best car within a price range of 3-5 lakhs. The answer is not equivalent\n \
                    Q: Question1: What ` s the best way to get rid of porn addiction ? Question2: 'What is the most effective way to break a porn addiction' ? Overall, what is the semantic relationship between the two questions? A: They both ask about the best or most effective way to overcome or eliminate a porn addiction. They use different phrasing, but the underlying meaning and intention of the questions are the same. Both questions seek advice or information on how to address and overcome a porn addiction. The answer is equivalent\n \
                    Q: [x] Overall, what is the semantic relationship between the two questions? A:"

COLA_COT = "Q: Sentence: 'That picture of Susan offended her.' Overall, is the given sentence grammatically correct? A: It follows a subject-verb-object structure, where 'That picture of Susan' is the subject, 'offended' is the verb, and 'her' is the object. The sentence is clear and coherent, conveying that the picture had an offensive impact on Susan. The answer is correct\n \
                    Q: Sentence: 'I enjoy yourself.' Overall, is the given sentence grammatically correct? A: The verb 'enjoy' is a transitive verb, which means it requires an object. In this case, the object should be a noun or a pronoun. However, 'yourself' is a reflexive pronoun, which cannot be used as the object of 'enjoy'. The answer is incorrect\n \
                    Q: [x] Overall, is the given sentence grammatically correct? A:"

COT_TEMPLATE = {"SNLI": SNLI_COT,
            "FEVER":FEVER_COT,
            "QQP": QQP_COT,
            "CoLA": COLA_COT,
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
        # prompt = TEMPLATE[task].replace("[x]",x)
        prompt = COT_TEMPLATE[task].replace("[x]",x)
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

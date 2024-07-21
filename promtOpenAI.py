import pandas as pd
from openai import OpenAI
import os
import csv
import random

userKey = "sk-None-NnH8o9ef3CO07qmwibo5T3BlbkFJ7yyMDUEoEkEvjcI8Ent2"
NUMOFQUESTIONS = 1000
fields = ['Math Question', 'Chat GPT Answer(str)', 'Chat GPT Answer(int)', 'Correct Answer', 'Was it correct?', 'Was it prompted?']
filename = 'chatbotOutput.csv'
client = OpenAI(api_key = userKey)

prompt = "You are a mathematician and are really good at arithmetic."
prompted = True

with open(filename, 'w', newline='') as file:                     #filewriter
    writer = csv.writer(file)
    writer.writerow(fields)

    for i in range(NUMOFQUESTIONS):                               #question creation logic
        if(prompted):
            prompted = False
        else:
            prompted = True
        sizeOfQuestion = [0] * random.randint(10,15)
        question = ""
        answer = 0
        for j in range(len(sizeOfQuestion)):
            addingNum = random.randint(1,10)
            question += str(addingNum)
            if(j<len(sizeOfQuestion)-1):
                question += "+"
            answer += addingNum
        question = "What's "+question+"?"


        if(prompted):
            chatbotOutput = client.chat.completions.create(             #openAI API
                model = "gpt-3.5-turbo",
                messages = [
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": question},
                ],
                temperature = 0,
            )
        else:
            chatbotOutput = client.chat.completions.create(
                model = "gpt-3.5-turbo",
                messages = [
                    {"role": "user", "content": question},
                ],
                temperature = 0,
            )

        chatbotAnswer = chatbotOutput.choices[0].message.content    #finds chatbot answer and converts to int
        chatbotAnswerInt = ''
        foundInt = False
        for i in range(len(chatbotAnswer), 0, -1):
            if (chatbotAnswer[i-1].isdigit()):
                chatbotAnswerInt += chatbotAnswer[i-1]
                foundInt = True
            else:
                if(foundInt):
                    break
        chatbotAnswerInt = int(chatbotAnswerInt[::-1])
        
        if(chatbotAnswerInt == answer):                             #checks is chatbot answer is correct
            wasItCorrect = True
        else:
            wasItCorrect = False

        writer.writerow([question, chatbotAnswer, str(chatbotAnswerInt), str(answer), str(wasItCorrect), str(prompted)])

    



#dataframebyrows = pd.DataFrame([('Ellis', 'F', 20, 'feldman.ellis@gmail.com', 130), 
#                                ('James', 'V', 20, 'james@gmail.com', 160)], 
#                      columns = ['Math Question', 'Chat GPT Answer(str)', 'Chat GPT Answer(int)', 'Correct Answer', 'Was it correct?', 'If Prompted', 'Prompt'])
#
#print(dataframebyrows)
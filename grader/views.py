from django.shortcuts import render
from django.core.files.storage import FileSystemStorage

#from django.http import HttpResponse
import json
import os
import pickle as pkl
import numpy as np
#import pandas as pd
#import matplotlib.pyplot as plt



# For single student grading
file_path = "/home/santhosh/django-apps/assistgrader/grader/multiple/"


    ## getting all the names of the file
file_list = list()
for file in os.listdir(file_path):
    if file.endswith(".ipynb"):
        file_list.append(file)
file_list = sorted(file_list)

## creating a dictionary of question anwers
ques_list = []
ques_ans_dict = {q:[] for q in np.arange(0,17)}

for ff in file_list:
    with open(file_path+ff) as f:
        data = json.load(f)
    ques_count = 0
    ans_list = []
    ques_list = []
    for i in range(len(data['cells'])):
        if 'nbgrader' in data['cells'][i]['metadata'] and (data['cells'][i]['metadata']['nbgrader']['solution'])==True:
            ques_ans_dict[ques_count].append((data['cells'][i]['source']))
            ques_count+=1
            ques_list.append ((data['cells'][i-1]['source']))
            if ques_count == 17:
                break

## ordering and cleaning answers
answer_list = []
for i in range(len(ques_ans_dict.keys())):
    for answers in ques_ans_dict[i]:
        answer_list.append(''.join(answers))
## ordering and cleaning questions
ques_list = [i[2] for i in ques_list for _ in range(len(ques_ans_dict[0]))]

final_dict = {'question':ques_list, 'student_answer':answer_list ,\
             'question_id':[i for i in range(1,18) for _ in range(len(ques_ans_dict[0]))],\
            'student_id':[i.split(".")[0] + str(j) for j in range(1,18) for i in file_list]}
#df = pd.DataFrame.from_dict(final_dict)
zipped_list = zip(ques_list,answer_list)

dict_zip = dict(zipped_list)
json_questions = json.dumps(ques_list)

ques_list_count = set(ques_list)

feedback = []    
for i in range(17): 
    feedback.append([])
    for n in range(39):
        feedback[i].append("")


 


def home(request):

	
	return render(request, 'grader/home.html')

def devfeed(request):

    return render(request, 'grader/devfeed.html')

def about(request):

    context = {
		'ques_list': ques_list,
		'answer_list': answer_list,
        'ques_list_count' : ques_list_count,
        'file_list'	: file_list,	
	}
    return render(request,'grader/about.html',context)

def main(request):

    context = {
            'ques_list': ques_list,
            'answer_list': answer_list,
            'ques_list_count' : ques_list_count,
            
    }
    return render(request,'grader/main.html',context)

def dev(request):

    context = {
        'ques_list': ques_list,
        'answer_list': answer_list,
        'ques_list_count' : ques_list_count,
        'file_list' : file_list,
        'feedback' : feedback, 
    }

    return render(request,'grader/dev.html', context)

def upload(request):
    if request.method == "POST":
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage(location = 'grader/single/')
        fs.save(uploaded_file.name, uploaded_file)
    return render(request,'grader/upload.html')

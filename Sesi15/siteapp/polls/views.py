from django.shortcuts import render
from django.http import HttpResponse
from .models import Question, Choice, Settings


def raw_index(request):
    question_list = Question.objects.all()
    output = ""

    for a in question_list:
        output += f"{a.question_text}<br>"
        #option list
        option_list = Choice.objects.filter(question=a)
        for b in option_list:
            output += f"{b.choice_text}<br>"
        output += "<br>"

    return HttpResponse(output)

def html_version(request):
    question_list = Question.objects.all()
    answer_list = Choice.objects.all()
    context = {
        "questions_option": question_list,
        "answers": answer_list
    }
    return render(request, "form.html", context)

def index_other(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    output = ""
    for q in latest_question_list:
        output += f"{q.question_text}<br>"
        #answer list
        answer_list = Choice.objects.filter(question=q)
        list_answer = ", ".join([a.choice_text for a in answer_list])
        output += f"Pilihan: {list_answer}"
        output += "<br><br>"
    return HttpResponse(output)

def html_index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    answer_list = Choice.objects.all()
    context = {
        "latest_question_list": latest_question_list,
        "answer_list": answer_list
    }
    return render(request, "index.html", context)

def profile(request):
    return HttpResponse("Hello, I Write other text here. You're at the polls profile.")

def contact(request):
    return HttpResponse("Please contact me at 085759402332")
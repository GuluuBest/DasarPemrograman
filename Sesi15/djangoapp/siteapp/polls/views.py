from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Question, Choice, Settings

def html_index(request):
    latest_question_list = Question.objects.order_by('-pub_date').prefetch_related('choice_set')[:5]
    context = { "latest_question_list": latest_question_list }
    return render(request, "polls/index.html", context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        context = {
            'question': question,
            'error_message': "Anda belum memilih salah satu pilihan.",
        }
        return render(request, 'polls/detail.html', context)
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})

def profile(request):
    return HttpResponse("Ini adalah halaman profil.")

def contact(request):
    return HttpResponse("Ini adalah halaman kontak.")
    
def address(request):
    return HttpResponse("Alamat saya di Kp Sundawenang Kecamatan Parungkuda")

def phone(request):
    return HttpResponse("Nomor telepon saya 085123669430")
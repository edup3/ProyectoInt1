from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse

# Create your views here.

def home(request):
    return render(request,'home.html')


from django.shortcuts import render, redirect
from .forms import FeedbackForm

def feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('thank_you')  # Redirige a una página de agradecimiento o de vuelta al inicio
    else:
        form = FeedbackForm()
    return render(request, 'feedback.html', {'form': form})

from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from . models import Task
from .forms import todoform
from django.views.generic import ListView
from django.views.generic import DetailView
from django.views.generic import UpdateView, DeleteView


class Tasklistview(ListView):
    model=Task
    template_name='home.html'
    context_object_name='tasks'

class TaskDetailview(DetailView):
    model=Task
    template_name='detail.html'
    context_object_name='tasks'

class TaskUpdateview(UpdateView):
    model=Task
    template_name='update.html'
    context_object_name='tasks'
    fields=('name','priority','date')

def get_success_url(self):
    return reverse_lazy('cbvdetail',kwargs={'pk':self.object.id})

class TaskDeleteview(DeleteView):
    model=Task
    template_name='delete.html'
    success_url=reverse_lazy('cbvhome')
# Create your views here.
def home(request):
    tasks=Task.objects.all()
    if request.method=='POST':
        name=request.POST.get('task','')
        priority=request.POST.get('priority','')
        date=request.POST.get('date','')
        task=Task(name=name,priority=priority,date=date)
        task.save()
    return render(request,'home.html',{'tasks':tasks})

#def details(request):
    
   # return render(request,'detail.html',)
def delete(request,taskid):
    task=Task.objects.get(id=taskid)
    if request.method=='POST':
        task.delete()
        return redirect('/')
    return render(request,'delete.html')

def update(request,id):
    tasks=Task.objects.get(id=id)
    f=todoform(request.POST or None,instance=tasks)
    if f.is_valid():
        f.save()
        return redirect('/')
    return render(request,'edit.html',{'f':f,'tasks':tasks})




from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from todoapp.form import TaskForm
from todoapp.models import Task
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView,DeleteView


# class based generic views
class TaskListView(ListView):
    model = Task
    template_name = 'home.html'
    context_object_name = 'task'
class TaskDetailView(DetailView):
    model = Task
    template_name = 'detail.html'
    context_object_name = 'task'

class TaskUpdateView(UpdateView):
    model = Task
    template_name = 'update.html'
    context_object_name = 'task'
    fields = ('name','priority','date')
    def get_success_url(self):
        return reverse_lazy('todoapp:cbvdetail',kwargs={'pk':self.object.id})

class TaskdeleteView(DeleteView):
    model = Task
    template_name = 'delete.html'
    success_url = reverse_lazy('todoapp:cbvhome')
# Create your views here.
def add(request):
    task1=Task.objects.all()

    if request.method == "POST":
        name = request.POST.get('name', )
        priority = request.POST.get('priority', )
        date = request.POST.get('date', )

        movie = Task(name=name, priority=priority, date=date)
        movie.save()
    return render(request,'home.html',{'task':task1})
def delete(request, id):
    if request.method=="POST":
        task = Task.objects.get(id=id)
        task.delete()
        return redirect('/')
    return render(request,'delete.html')

def update(request, id):
    task=Task.objects.get(id=id)
    form=TaskForm(request.POST or None,instance=task)
    if form.is_valid():
        form.save()
        return redirect('/')
    return render(request,'edit.html',{'f':form,'task':task})

# def detail(request):
#     task=Task.objects.all()
#     return render(request,'detail.html', {'task':task})

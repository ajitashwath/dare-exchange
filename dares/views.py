from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Dare

class DareListView(ListView):
    model = Dare
    template_name = 'dare_list.html'
    context_object_name = 'dares'

class DareDetailView(DetailView):
    model = Dare
    template_name = 'dare_detail.html'
    context_object_name = 'dare'

class DareCreateView(CreateView):
    model = Dare
    template_name = 'dare_form.html'
    fields = ['name', 'phone_number', 'college', 'dare_text']
    success_url = reverse_lazy('dare_list')

class DareUpdateView(UpdateView):
    model = Dare
    template_name = 'dare_form.html'
    fields = ['name', 'phone_number', 'college', 'dare_text']
    success_url = reverse_lazy('dare_list')

class DareDeleteView(DeleteView):
    model = Dare
    template_name = 'dare_confirm_delete.html'
    context_object_name = 'dare'
    success_url = reverse_lazy('dare_list')

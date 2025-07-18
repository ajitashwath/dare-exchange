from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages

from .models import Dare
from .forms import DareForm

class DareListView(ListView):
    model = Dare
    template_name = 'dare_list.html'
    context_object_name = 'dares'
    paginate_by = 6

class DareDetailView(DetailView):
    model = Dare
    template_name = 'dare_detail.html'
    context_object_name = 'dare'

class DareCreateView(SuccessMessageMixin, CreateView):
    model = Dare
    form_class = DareForm
    template_name = 'dare_form.html'
    success_url = reverse_lazy('dare_list')
    success_message = "🎉 Dare was created successfully!"

class DareUpdateView(SuccessMessageMixin, UpdateView):
    model = Dare
    form_class = DareForm
    template_name = 'dare_form.html'
    success_url = reverse_lazy('dare_list')
    success_message = "✅ Dare was updated successfully!"

class DareDeleteView(DeleteView):
    model = Dare
    template_name = 'dare_confirm_delete.html'
    context_object_name = 'dare'
    success_url = reverse_lazy('dare_list')

    def form_valid(self, form):
        messages.success(self.request, "🗑️ Dare was deleted successfully.")
        return super().form_valid(form)

"""Views for homework management app."""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.db.models import Q
from .models import Homework, Subject, Submission
from .forms import HomeworkForm, SubmissionForm


@login_required
def home(request):
    """Home page showing homework dashboard."""
    my_assignments = Homework.objects.filter(assigned_to=request.user).order_by('-due_date')[:5]
    pending_submissions = Submission.objects.filter(
        student=request.user,
        status='submitted'
    ).select_related('homework').order_by('-submitted_at')[:5]
    
    context = {
        'my_assignments': my_assignments,
        'pending_submissions': pending_submissions,
    }
    return render(request, 'homework/home.html', context)


class HomeworkListView(LoginRequiredMixin, ListView):
    """List all homeworks assigned to the user."""
    model = Homework
    template_name = 'homework/homework_list.html'
    context_object_name = 'homeworks'
    paginate_by = 10

    def get_queryset(self):
        return Homework.objects.filter(assigned_to=self.request.user).select_related('subject')


class HomeworkDetailView(LoginRequiredMixin, DetailView):
    """Display details of a specific homework."""
    model = Homework
    template_name = 'homework/homework_detail.html'
    context_object_name = 'homework'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        homework = self.get_object()
        try:
            submission = Submission.objects.get(homework=homework, student=self.request.user)
            context['submission'] = submission
        except Submission.DoesNotExist:
            context['submission'] = None
        return context


class HomeworkCreateView(LoginRequiredMixin, CreateView):
    """Create a new homework assignment."""
    model = Homework
    form_class = HomeworkForm
    template_name = 'homework/homework_form.html'
    success_url = reverse_lazy('homework_list')

    def form_valid(self, form):
        form.instance.assigned_by = self.request.user
        return super().form_valid(form)


class SubmissionCreateView(LoginRequiredMixin, CreateView):
    """Submit homework by a student."""
    model = Submission
    form_class = SubmissionForm
    template_name = 'homework/submission_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        homework_id = self.kwargs.get('homework_id')
        context['homework'] = get_object_or_404(Homework, id=homework_id)
        return context

    def form_valid(self, form):
        homework = get_object_or_404(Homework, id=self.kwargs.get('homework_id'))
        form.instance.homework = homework
        form.instance.student = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('homework_detail', kwargs={'pk': self.kwargs.get('homework_id')})

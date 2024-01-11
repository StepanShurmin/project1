from django.conf import settings
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.core.cache import cache
from django.forms import inlineformset_factory
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView

from main.forms import StudentForm, SubjectForm
from main.models import Student, Subject
from main.services import get_cached_subjects_for_student


@login_required
@permission_required('main.view_student')
def index(request):
    students_list = Student.objects.all()
    context = {'object_list': students_list,
               'title': 'Главная'
               }
    return render(request, 'main/index.html', context)


@login_required
def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        print(f'{name} {email} {message}')

    context = {
        'title': 'Контакты'
    }
    return render(request, 'main/contact.html', context=context)


class StudentDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Student
    permission_required = 'main.view_student'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        context_data['subjects'] = get_cached_subjects_for_student(self.object.pk)
        return context_data


class StudentCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Student
    form_class = StudentForm
    permission_required = 'main.add_student'
    success_url = reverse_lazy('main:index')


class StudentUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Student
    form_class = StudentForm
    permission_required = 'main.change_student'
    success_url = reverse_lazy('main:index')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        SubjectFormset = inlineformset_factory(Student, Subject, form=SubjectForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = SubjectFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = SubjectFormset(instance=self.object)
        return context_data

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()

        return super().form_valid(form)


class StudentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Student
    # permission_required = 'main.delete_student' права на удаление если использовать PermissionRequiredMixin вместо UserPassesTestMixin и def test_func
    success_url = reverse_lazy('main:index')

    def test_func(self):
        return self.request.user.is_superuser

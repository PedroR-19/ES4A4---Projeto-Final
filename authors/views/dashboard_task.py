from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http.response import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View

from authors.forms.task_form import AuthorTaskForm
from tasks.models import Task


@method_decorator(
    login_required(login_url='authors:login', redirect_field_name='next'),
    name='dispatch'
)
class DashboardTask(View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def setup(self, *args, **kwargs):
        return super().setup(*args, **kwargs)

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_task(self, id=None):
        task = None

        if id is not None:
            task = Task.objects.filter(
                is_published=False,
                author=self.request.user,
                pk=id,
            ).first()

            if not task:
                raise Http404()

        return task

    def render_task(self, form):
        return render(
            self.request,
            'authors/pages/dashboard_task.html',
            context={
                'form': form
            }
        )

    def get(self, request, id=None):
        task = self.get_task(id)
        form = AuthorTaskForm(instance=task)
        return self.render_task(form)

    def post(self, request, id=None):
        task = self.get_task(id)
        form = AuthorTaskForm(
            data=request.POST or None,
            files=request.FILES or None,
            instance=task
        )

        if form.is_valid():
            # Agora, o form é válido e eu posso tentar salvar
            task = form.save(commit=False)

            task.author = request.user
            task.steps_is_html = False
            task.is_published = False

            task.save()

            messages.success(request, 'Sua receita foi salva com sucesso!')
            return redirect(
                reverse(
                    'authors:dashboard_task_edit', args=(
                        task.id,
                    )
                )
            )

        return self.render_task(form)


@method_decorator(
    login_required(login_url='authors:login', redirect_field_name='next'),
    name='dispatch'
)
class DashboardTaskDelete(DashboardTask):
    def post(self, *args, **kwargs):
        task = self.get_task(self.request.POST.get('id'))
        task.delete()
        messages.success(self.request, 'Deleted successfully.')
        return redirect(reverse('authors:dashboard'))

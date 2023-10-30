from django.urls import resolve, reverse
from tasks import views

from .test_task_base import TaskTestBase


class TaskDetailViewTest(TaskTestBase):
    def test_task_detail_view_function_is_correct(self):
        view = resolve(
            reverse('tasks:task', kwargs={'pk': 1})
        )
        self.assertIs(view.func.view_class, views.TaskDetail)

    def test_task_detail_view_returns_404_if_no_tasks_found(self):
        response = self.client.get(
            reverse('tasks:task', kwargs={'pk': 1000})
        )
        self.assertEqual(response.status_code, 404)

    def test_task_detail_template_loads_the_correct_task(self):
        needed_title = 'This is a detail page - It load one task'

        # Need a task for this test
        self.make_task(title=needed_title)

        response = self.client.get(
            reverse(
                'tasks:task',
                kwargs={
                    'pk': 1
                }
            )
        )
        content = response.content.decode('utf-8')

        # Check if one task exists
        self.assertIn(needed_title, content)

    def test_task_detail_template_dont_load_task_not_published(self):
        """Test task is_published False dont show"""
        # Need a task for this test
        task = self.make_task(is_published=False)

        response = self.client.get(
            reverse(
                'tasks:task',
                kwargs={
                    'pk': task.id
                }
            )
        )

        self.assertEqual(response.status_code, 404)

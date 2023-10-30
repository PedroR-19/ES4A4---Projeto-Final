from django.urls import resolve, reverse
from tasks import views

from .test_task_base import TaskTestBase


class TaskCategoryViewTest(TaskTestBase):
    def test_task_category_view_function_is_correct(self):
        view = resolve(
            reverse('tasks:category', kwargs={'category_id': 1000})
        )
        self.assertIs(view.func.view_class, views.TaskListViewCategory)

    def test_task_category_view_returns_404_if_no_tasks_found(self):
        response = self.client.get(
            reverse('tasks:category', kwargs={'category_id': 1000})
        )
        self.assertEqual(response.status_code, 404)

    def test_task_category_template_loads_tasks(self):
        needed_title = 'This is a category test'
        # Need a task for this test
        self.make_task(title=needed_title)

        response = self.client.get(reverse('tasks:category', args=(1,)))
        content = response.content.decode('utf-8')

        # Check if one task exists
        self.assertIn(needed_title, content)

    def test_task_category_template_dont_load_tasks_not_published(self):
        """Test task is_published False dont show"""
        # Need a task for this test
        task = self.make_task(is_published=False)

        response = self.client.get(
            reverse('tasks:task', kwargs={'pk': task.category.id})
        )

        self.assertEqual(response.status_code, 404)

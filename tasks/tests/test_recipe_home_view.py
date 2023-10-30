from unittest.mock import patch

from django.urls import resolve, reverse
from tasks import views

from .test_task_base import TaskTestBase


class TaskHomeViewTest(TaskTestBase):
    def test_task_home_view_function_is_correct(self):
        view = resolve(reverse('tasks:home'))
        self.assertIs(view.func.view_class, views.TaskListViewHome)

    def test_task_home_view_returns_status_code_200_OK(self):
        response = self.client.get(reverse('tasks:home'))
        self.assertEqual(response.status_code, 200)

    def test_task_home_view_loads_correct_template(self):
        response = self.client.get(reverse('tasks:home'))
        self.assertTemplateUsed(response, 'tasks/pages/home.html')

    def test_task_home_template_shows_no_tasks_found_if_no_tasks(self):
        response = self.client.get(reverse('tasks:home'))
        self.assertIn(
            '<h1>No tasks found here 🥲</h1>',
            response.content.decode('utf-8')
        )

    def test_task_home_template_loads_tasks(self):
        # Need a task for this test
        self.make_task()

        response = self.client.get(reverse('tasks:home'))
        content = response.content.decode('utf-8')
        response_context_tasks = response.context['tasks']

        # Check if one task exists
        self.assertIn('Task Title', content)
        self.assertEqual(len(response_context_tasks), 1)

    def test_task_home_template_dont_load_tasks_not_published(self):
        """Test task is_published False dont show"""
        # Need a task for this test
        self.make_task(is_published=False)

        response = self.client.get(reverse('tasks:home'))

        # Check if one task exists
        self.assertIn(
            '<h1>No tasks found here 🥲</h1>',
            response.content.decode('utf-8')
        )

    def test_task_home_is_paginated(self):
        self.make_task_in_batch(qtd=8)

        with patch('tasks.views.PER_PAGE', new=3):
            response = self.client.get(reverse('tasks:home'))
            tasks = response.context['tasks']
            paginator = tasks.paginator

            self.assertEqual(paginator.num_pages, 3)
            self.assertEqual(len(paginator.get_page(1)), 3)
            self.assertEqual(len(paginator.get_page(2)), 3)
            self.assertEqual(len(paginator.get_page(3)), 2)

    def test_invalid_page_query_uses_page_one(self):
        self.make_task_in_batch(qtd=8)

        with patch('tasks.views.PER_PAGE', new=3):
            response = self.client.get(reverse('tasks:home') + '?page=12A')
            self.assertEqual(
                response.context['tasks'].number,
                1
            )
            response = self.client.get(reverse('tasks:home') + '?page=2')
            self.assertEqual(
                response.context['tasks'].number,
                2
            )
            response = self.client.get(reverse('tasks:home') + '?page=3')
            self.assertEqual(
                response.context['tasks'].number,
                3
            )

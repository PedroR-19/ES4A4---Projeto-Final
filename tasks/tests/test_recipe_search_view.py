from django.urls import resolve, reverse
from tasks import views

from .test_task_base import TaskTestBase


class TaskSearchViewTest(TaskTestBase):
    def test_task_search_uses_correct_view_function(self):
        resolved = resolve(reverse('tasks:search'))
        self.assertIs(resolved.func.view_class, views.TaskListViewSearch)

    def test_task_search_loads_correct_template(self):
        response = self.client.get(reverse('tasks:search') + '?q=teste')
        self.assertTemplateUsed(response, 'tasks/pages/search.html')

    def test_task_search_raises_404_if_no_search_term(self):
        url = reverse('tasks:search')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_task_search_term_is_on_page_title_and_escaped(self):
        url = reverse('tasks:search') + '?q=<Teste>'
        response = self.client.get(url)
        self.assertIn(
            'Search for &quot;&lt;Teste&gt;&quot;',
            response.content.decode('utf-8')
        )

    def test_task_search_can_find_task_by_title(self):
        title1 = 'This is task one'
        title2 = 'This is task two'

        task1 = self.make_task(
            slug='one', title=title1, author_data={'username': 'one'}
        )
        task2 = self.make_task(
            slug='two', title=title2, author_data={'username': 'two'}
        )

        search_url = reverse('tasks:search')
        response1 = self.client.get(f'{search_url}?q={title1}')
        response2 = self.client.get(f'{search_url}?q={title2}')
        response_both = self.client.get(f'{search_url}?q=this')

        self.assertIn(task1, response1.context['tasks'])
        self.assertNotIn(task2, response1.context['tasks'])

        self.assertIn(task2, response2.context['tasks'])
        self.assertNotIn(task1, response2.context['tasks'])

        self.assertIn(task1, response_both.context['tasks'])
        self.assertIn(task2, response_both.context['tasks'])

from django.test import TestCase
from django.urls import reverse


class TaskURLsTest(TestCase):
    def test_task_home_url_is_correct(self):
        url = reverse('tasks:home')
        self.assertEqual(url, '/')

    def test_task_category_url_is_correct(self):
        url = reverse('tasks:category', kwargs={'category_id': 1})
        self.assertEqual(url, '/tasks/category/1/')

    def test_task_detail_url_is_correct(self):
        url = reverse('tasks:task', kwargs={'pk': 1})
        self.assertEqual(url, '/tasks/1/')

    def test_task_search_url_is_correct(self):
        url = reverse('tasks:search')
        self.assertEqual(url, '/tasks/search/')

# RED - GREEN - REFACTOR

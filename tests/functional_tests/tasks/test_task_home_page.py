from unittest.mock import patch

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from .base import TaskBaseFunctionalTest


@pytest.mark.functional_test
class TaskHomePageFunctionalTest(TaskBaseFunctionalTest):
    def test_task_home_page_without_tasks_not_found_message(self):
        self.browser.get(self.live_server_url)
        body = self.browser.find_element(By.TAG_NAME, 'body')
        self.assertIn('No tasks found here 🥲', body.text)

    @patch('tasks.views.PER_PAGE', new=2)
    def test_task_search_input_can_find_correct_tasks(self):
        tasks = self.make_task_in_batch()

        title_needed = 'This is what I need'

        tasks[0].title = title_needed
        tasks[0].save()

        # Usuário abre a página
        self.browser.get(self.live_server_url)

        # Vê um campo de busca com o texto "Search for a task"
        search_input = self.browser.find_element(
            By.XPATH,
            '//input[@placeholder="Search for a task"]'
        )

        # Clica neste input e digita o termo de busca
        # para encontrar a receita o título desejado
        search_input.send_keys(title_needed)
        search_input.send_keys(Keys.ENTER)

        # O usuário vê o que estava procurando na página
        self.assertIn(
            title_needed,
            self.browser.find_element(By.CLASS_NAME, 'main-content-list').text,
        )

    @patch('tasks.views.PER_PAGE', new=2)
    def test_task_home_page_pagination(self):
        self.make_task_in_batch()

        # Usuário abre a página
        self.browser.get(self.live_server_url)

        # Vê que tem uma paginação e clica na página 2
        page2 = self.browser.find_element(
            By.XPATH,
            '//a[@aria-label="Go to page 2"]'
        )
        page2.click()

        # Vê que tem mais 2 receitas na página 2
        self.assertEqual(
            len(self.browser.find_elements(By.CLASS_NAME, 'task')),
            2
        )

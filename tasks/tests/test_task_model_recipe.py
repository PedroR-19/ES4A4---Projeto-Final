from django.core.exceptions import ValidationError
from parameterized import parameterized

from .test_task_base import Task, TaskTestBase


class TaskModelTest(TaskTestBase):
    def setUp(self) -> None:
        self.task = self.make_task()
        return super().setUp()

    def make_task_no_defaults(self):
        task = Task(
            category=self.make_category(name='Test Default Category'),
            author=self.make_author(username='newuser'),
            title='Task Title',
            description='Task Description',
            slug='task-slug-for-no-defaults',
            time=10,
            time_unit='Minutos',
            servings=5,
            servings_unit='Porções',
            steps='Task Preparation Steps',
        )
        task.full_clean()
        task.save()
        return task

    @parameterized.expand([
        ('title', 65),
        ('description', 165),
        ('time_unit', 65),
        ('servings_unit', 65),
    ])
    def test_task_fields_max_length(self, field, max_length):
        setattr(self.task, field, 'A' * (max_length + 1))
        with self.assertRaises(ValidationError):
            self.task.full_clean()

    def test_task_steps_is_html_is_false_by_default(self):
        task = self.make_task_no_defaults()
        self.assertFalse(
            task.steps_is_html,
            msg='Task steps_is_html is not False',
        )

    def test_task_is_published_is_false_by_default(self):
        task = self.make_task_no_defaults()
        self.assertFalse(
            task.is_published,
            msg='Task is_published is not False',
        )

    def test_task_string_representation(self):
        needed = 'Testing Representation'
        self.task.title = needed
        self.task.full_clean()
        self.task.save()
        self.assertEqual(
            str(self.task), needed,
            msg=f'Task string representation must be '
                f'"{needed}" but "{str(self.task)}" was received.'
        )

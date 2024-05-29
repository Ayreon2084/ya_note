from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from notes.forms import NoteForm
from notes.models import Note

User = get_user_model()


class TestContent(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(
            username='Author',
        )
        cls.auth_user = User.objects.create(
            username='Random user',
        )
        cls.note = Note.objects.create(
            title='Title',
            text='Text',
            author=cls.author,
        )


    def test_not_authorized_user_has_no_form(self):
        urls = (
            ('notes:edit', self.note.slug),
            ('notes:detail', self.note.slug),
        )

        for name, kwargs in urls:
            with self.subTest(name=name):
                response = self.client.get(name, kwargs=kwargs)
                self.assertNotIn('form', response.context)

    def test_create_note_form_available_for_authorized_users(self):
        url = reverse('notes:add')
        self.client.force_login(self.auth_user)
        response = self.client.get(url)
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], NoteForm)

    def test_edit_note_form_available_for_author(self):
        url = reverse('notes:edit', kwargs={'slug': self.note.slug})
        self.client.force_login(self.author)
        response = self.client.get(url)
        self.assertIn('note', response.context)
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], NoteForm)
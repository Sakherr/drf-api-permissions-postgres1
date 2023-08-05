from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Wizard


class WizardTests(APITestCase):
   
    @classmethod
    def setUpTestData(cls):
        testuser1 = get_user_model().objects.create_user(
            username="testuser1", password="pass"
        )
        testuser1.save()

        test_wizard = Wizard.objects.create(
            name="Draco Malfoy",
            creator=testuser1,
            source = 'Harry Potter',
            about="loser whiny blonde boy",
        )
        test_wizard.save()

    def setUp(self):
        self.client.login(username='testuser1', password='pass')

    def test_wizards_model(self):
        wizard = Wizard.objects.get(id=1)
        actual_creator = str(wizard.creator)
        actual_name = str(wizard.name)
        actual_about = str(wizard.about)
        actual_source = str(wizard.source)
        self.assertEqual(actual_creator, "testuser1")
        self.assertEqual(actual_name, "Draco Malfoy")
        self.assertEqual(actual_source, "Harry Potter")
        self.assertEqual(
            actual_about, "loser whiny blonde boy"
        )

    def test_get_wizard_list(self):
        url = reverse("wizard_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        wizards = response.data
        self.assertEqual(len(wizards), 1)
        self.assertEqual(wizards[0]["name"], "Draco Malfoy")

    def test_get_wizard_by_id(self):
        url = reverse("wizard_detail", args=(1,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        wizard = response.data
        self.assertEqual(wizard["name"], "Draco Malfoy")

    def test_create_wizard(self):
        url = reverse("wizard_list")
        data = {"creator": 1, "name": "Big Hat Logan", "about": "sells spells", "source": "Dark Souls"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        wizards = Wizard.objects.all()
        self.assertEqual(len(wizards), 2)
        self.assertEqual(Wizard.objects.get(id=2).name, "Big Hat Logan")

    def test_update_wizard(self):
        url = reverse("wizard_detail", args=(1,))
        data = {
            "creator": 1,
            "name": "Draco Malfoy",
            "about": "kinda became alright towards the end i guess.",
            "source": "Harry Potter"
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        wizard = Wizard.objects.get(id=1)
        self.assertEqual(wizard.name, data["name"])
        self.assertEqual(wizard.creator.id, data["creator"])
        self.assertEqual(wizard.about, data["about"])

    def test_delete_wizard(self):
        url = reverse("wizard_detail", args=(1,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        wizards = Wizard.objects.all()
        self.assertEqual(len(wizards), 0)

    def test_authentication_required(self):
        self.client.logout()
        url = reverse("wizard_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

import json

from django.test import TestCase
from rest_framework.test import RequestsClient

from Core.models import SCTFUser

baseURL = "http://localhost:8000/"
apiURL = baseURL + "api/"

# Create your tests here.
class SCTFUserAPITest(TestCase):
    @classmethod
    def setUpClass(self):
        self.client = RequestsClient()

        self.u = SCTFUser.objects.create(
            username="TestUser1"
        )
        self.u.set_password("TestPassword")
        self.u.is_verified = True
        self.u.save()

        resp = self.client.post(baseURL+"auth/login", data={
            "username": "TestUser1",
            "password": "TestPassword"
        })

        if resp.status_code != 200:
            raise Exception('Failed to authenticate user with status: ' + str(resp.status_code))
        data = json.loads(resp.content)
        print(data["token"])
        self.token = f"Token {data['token']}"

    @classmethod
    def tearDownClass(self):
        self.u.delete()

    def test_anonymous_create_user(self):
        resp = self.client.post(apiURL + "users/", data={
            "username": "TestUser2",
            "password": "TestPassword"
        })

        self.assertEqual(resp.status_code, 201)
        data = json.loads(resp.content)
        self.assertTrue(SCTFUser.objects.filter(pk=data["id"]).exists())
    
    def test_anonymous_endpoint_access_get(self):
        self.assertEqual(
            self.client.get(apiURL + "users/").status_code,
            401
        )

    def test_anonymous_endpoint_access_put(self):
        self.assertEqual(
            self.client.put(apiURL + f"users/{self.u.id}/", data={
                "username": "TestUser2",
                "password": "TestPassword"
                }).status_code,
            401
        )

    def test_anonymous_endpoint_access_delete(self):
        self.assertEqual(
            self.client.delete(apiURL + f"users/{self.u.id}/").status_code,
            401
        )
    
    def test_anonymous_login(self):
        resp = self.client.post(baseURL + "auth/login", data={
            "username": "TestUser1",
            "password": "TestPassword"
        })
        self.assertEqual(resp.status_code, 200)

    def test_correct_user_get(self):
        self.client.headers.update({'Authorization': self.token})
        resp = self.client.get(apiURL + f"users/{self.u.id}/")
        self.assertEqual(resp.status_code, 200)

        d = json.loads(data.content)
        self.assertEqual(d["username"], u.username)
        self.assertEqual(d["first_name"], u.first_name)
        self.assertEqual(d["last_name"], u.last_name)
        self.assertEqual(d["display_name"], u.display_name)
        
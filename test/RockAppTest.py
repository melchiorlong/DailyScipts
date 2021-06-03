import unittest
from service.rock_app_service import app


class RockAppTest():

    @classmethod
    def setUpClass(cls):
        cls.app = app.flaskapp.test_client()
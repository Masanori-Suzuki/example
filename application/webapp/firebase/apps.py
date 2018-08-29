from django.apps import AppConfig

import firebase_admin
from firebase_admin import credentials

class FirebaseConfig(AppConfig):
    name = 'firebase'

    def ready(self):
        cred = credentials.Certificate('/Users/suzuki/pythonProject/example/application/webapp/example-96769-firebase-adminsdk-g74y0-89531c9764.json')
        default_app = firebase_admin.initialize_app(cred)

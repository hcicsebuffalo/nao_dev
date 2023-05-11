from django.http import JsonResponse
from firebase_admin import firestore

def get_users(request):
    users = []
    docs = firestore.client().collection('users').get()
    for doc in docs:
        users.append(doc.to_dict())

    return JsonResponse({'users': users})
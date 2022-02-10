from django.contrib.auth.models import User
from random import randint, choice
from django.utils import timezone
from datetime import timedelta
from manage_docs.models import Document, Client, RelationshipManager

def random_user():
    names_list = ['Jared', 'Lyric', 'Elvis', 'Clarissa', 'Trevin', 'Davin', 'Luz', 'Talia', 'Shaylee', 'Eve', 'Tony', 'Elliana']
    surname_list = ['Pierce', 'Barry', 'Mack', 'Miranda', 'Shaw', 'Boyd', 'Francis', 'Jordan', 'Huynh', 'Caldwell', 'Good', 'Bruce']
    chosen_name = choice(names_list)
    chosen_surname = choice(surname_list)
    random_time = timezone.now() - timedelta(
        seconds=randint(1,10000), minutes=randint(1,300), hours=randint(1,5)
        )
    user = User.objects.create_user(
            username='{}{}'.format(chosen_name, randint(1,6969)), 
            email='{}{}@{}.com'.format(chosen_name, randint(1,42), chosen_surname), 
            first_name=chosen_name,
            last_name=chosen_surname,
            last_login=random_time,
            date_joined=random_time-timedelta(minutes=randint(1,420))
        )
    return user

def random_rm():
    rm = RelationshipManager.objects.create(
        user = random_user()
    )
    return rm

def random_client(rm):
    client = Client.objects.create(
        user = random_user(),
        relationship_manager = rm
    )
    return client

def random_document(client, name_exclude):
    demo_document_types = ['ID', 'Passport', 'Proof of address', 'Bank statement', 'Birth certificate', 'Tax certificate']
    demo_document_types = list(set(demo_document_types)- set(name_exclude))
    doc = Document.objects.create(
        name = choice(demo_document_types),
        client = client
    )
    return doc

def add_data():
    for k in range(randint(2,5)):
        rm = random_rm()
        for i in range(randint(1, 10)):
            cl = random_client(rm)
            taken_doc_names = []
            for j in range(randint(1, 6)):
                d = random_document(cl, taken_doc_names)
                taken_doc_names.append(d.name)
    print("Added demo data...")

def run():
    add_data()
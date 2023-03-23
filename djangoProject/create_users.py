from django.contrib.auth.models import User

users = ["Gonçalo", "Vasco", "Nuno"] #adicioaraqui users para criação


def create_sample_users():
    for name in users:
        mail = name.lower() + "@iscte.pt"
        password = "pass"
        User.objects.create_user(name, mail, password)


create_sample_users()

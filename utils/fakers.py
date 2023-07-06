from faker import Faker

fake = Faker()


def fake_name():
    return fake.name()

import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here

from main_app.models import Pet, Artifact, Location, Car, Task

# Create queries within functions


def create_pet(name, species):
    Pet.objects.create(name=name, species=species)
    return f"{name} is a very cute {species}!"


def create_artifact(name, origin, age, description, is_magical):
    Artifact.objects.create(
        name=name,
        origin=origin,
        age=age,
        description=description,
        is_magical=is_magical
    )

    return f"The artifact {name} is {age} years old!"


def delete_all_artifacts():
    Artifact.objects.all().delete()


def show_all_locations():
    locations = Location.objects.all().order_by('-id')

    location_info = []

    for location in locations:
        location_info.append(f"{location.name} has a population of {location.population}!")

    return '\n'.join(location_info)


def new_capital():
    location = Location.objects.first()

    location.is_capital = True

    location.save()


def get_capitals():
    return Location.objects.filter(is_capital=True).values('name')


def delete_first_location():
    Location.objects.first().delete()


def apply_discount():
    cars = Car.objects.all()

    for car in cars:
        percent_of_disc = sum(int(x) for x in str(car.year)) / 100
        car.price_with_discount = float(car.price) - (float(car.price) * percent_of_disc)
        car.save()


def get_recent_cars():
    return Car.objects.filter(year__gte=2020).values('model', 'price_with_discount')


def delete_last_car():
    Car.objects.last().delete()


def show_unfinished_tasks():
    tasks = Task.objects.filter(is_finished=False)

    for task in tasks:
        print(f"Task - {task.title} needs to be done until {task.due_date}!")


def complete_odd_tasks():
    for task in Task.objects.all():
        if task.id % 2 != 0:
            task.is_finished = True
            task.save()


def encode_and_replace(text, task_title):
    new_description = ''

    for char in text:
        new_description += chr(ord(char) - 3)

    Task.objects.filter(title=task_title).update(description=new_description)

    # for task in Task.objects.filter(title=task_title):
    #     task.description = new_description
    #     task.save()











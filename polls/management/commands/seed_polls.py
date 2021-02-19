import random

from django.core.management.base import BaseCommand
from django.contrib.admin.utils  import flatten
from django_seed                 import Seed

from django.contrib.auth.models  import User
from polls.models                import Poll,Choice,Vote


class Command(BaseCommand):

    help = "This command generated users, polls, choices"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number", default=1, type=int, help="How many do you want create users, polls, choices"
        )

    def handle(self, *args, **options):
        number = int(options.get("number"))
        seeder = Seed.seeder()
        seeder.add_entity(User, number, {"is_staff" : False, "is_superuser": False,})
        seeder.add_entity(Poll,number, {"created_by": lambda x : random.choice(User.objects.select_related()), })
        seeder.add_entity(Choice,number,{"poll"     : lambda x : random.choice(Poll.objects.select_related()),})
    
        inserted_pk = seeder.execute()
        users, polls, choices = inserted_pk.keys()

        for i in range(number):
            Vote.objects.create(
                choice   = Choice.objects.get(pk=inserted_pk[choices][i]),
                poll     = Poll.objects.get(pk=inserted_pk[polls][i]),
                voted_by = User.objects.get(pk=inserted_pk[users][i]),
                )
             
         

        self.stdout.write(self.style.SUCCESS(f"{number} users, {number} polls, {number} choices, {number} votes created!"))
import calendar
import random
from datetime import date, timedelta
from random import randint

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from ask.models import Question, Answer, Tag


def random_date():
    first_jan = date.today().replace(day=1, month=1)
    return first_jan + timedelta(days=random.randint(0, 365 if calendar.isleap(first_jan.year) else 364))


class Command(BaseCommand):
    def handle(self, *args, **options):
        for i in range(10):
            user = User.objects.create_user('user' + str(i), password=str(i))
            user.save()
        for i in range(100):
            question = Question(title='Question#{}'.format(i),
                                text='Cras vel lacus vulputate, dapibus lorem eget, ullamcorper orci. Duis ac erat non velit egestas convallis. Phasellus sapien nulla, dignissim et purus vitae, accumsan maximus tortor. Integer lobortis eget dolor sed pellentesque. Nullam fermentum enim nibh, id efficitur nunc convallis id. Vestibulum non pellentesque justo. Cras non erat sed lacus vestibulum dictum. Sed venenatis nulla ipsum, sed ultricies risus ultricies vitae.',
                                author=User.objects.get(pk=randint(1, 10)),
                                date=random_date())
            question.save()
            for j in range(10):
                answer = Answer(text='Cras vel lacus vulputate, dapibus lorem eget, ullamcorper orci.\
                                Duis ac erat non velit egestas convallis.\
                                Phasellus sapien nulla, dignissim et purus vitae, accumsan maximus tortor.\
                                Integer lobortis eget dolor sed pellentesque.\
                                Nullam fermentum enim nibh, id efficitur nunc convallis id.\
                                Vestibulum non pellentesque justo. Cras non erat sed lacus vestibulum dictum.\
                                Sed venenatis nulla ipsum, sed ultricies risus ultricies vitae.',
                                author=User.objects.get(pk=randint(1, 10)),
                                question=question)
                answer.save()
        for i in 'lorem ipsum dolor sit amet elit cras vitae urna leo sed molestie vestibulum nulla odio cursus tortor euismod nec ornare dolor molestie fusce suscipit metus magna nisl tempor velit mattis orci felis at lacus'.split():
            if len(Tag.objects.filter(name=i)) == 0:
                tag = Tag(name=i)
                tag.save()
        tags = Tag.objects.all()
        for i in Question.objects.all():
            for tag in tags:
                if randint(1, 10) == 10:
                    i.tags.add(tag)

import datetime

from django.db import models

from django.contrib.auth.models import User


class QuestionModel(models.Manager):
    def new(self):
        return Question.objects.order_by('-date')

    def hot(self):
        return Question.objects.order_by('-rating')

    def new_tag(self, tag):
        return Tag.objects.get(name=tag).question_set.order_by('-date')

    def hot_tag(self, tag):
        return Tag.objects.get(name=tag).question_set.order_by('-rating')


class TagModel(models.Manager):
    def popular_tags(self):
        return Tag.objects.all()[:5]


class Tag(models.Model):
    name = models.CharField(max_length=15, unique=True)
    objects = TagModel()


class Question(models.Model):
    title = models.CharField(max_length=128)
    text = models.TextField()
    date = models.DateTimeField(default=datetime.datetime.now)
    author = models.ForeignKey(User)
    rating = models.IntegerField(default=0)
    tags = models.ManyToManyField(Tag)
    picture = models.ImageField(upload_to='uploads/', default='uploads/default_avatar.jpg')
    objects = QuestionModel()


class Answer(models.Model):
    text = models.TextField()
    author = models.ForeignKey(User)
    question = models.ForeignKey(Question)


class Profile(models.Model):
    user = models.OneToOneField(User)
    avatar = models.ImageField(upload_to='uploads/', default='uploads/default_avatar.jpg')
    rating = models.IntegerField(default=0)


class Like(models.Model):
    user = models.ForeignKey(User)
    question = models.ForeignKey(Question)
    like = models.BooleanField(default=True)

    class Meta:
        unique_together = ("user", "question")
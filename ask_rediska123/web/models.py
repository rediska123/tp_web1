from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count

class profile(models.Model):
    user = models.OneToOneField(User, verbose_name=("user"), on_delete=models.CASCADE)
    avatar = models.ImageField(("avatar"), upload_to="uploads", height_field=None, width_field=None, max_length=None)
    rating = models.IntegerField(("rating"))
    class Meta:
        verbose_name = ("Profile")
        verbose_name_plural = ("Profiles")

    def __str__(self):
        return self.user.username

class tag(models.Model):
    name = models.CharField(("tag"), max_length=100)
    class Meta:
        verbose_name = ("tag")
        verbose_name_plural = ("tags")
        
    def __str__(self):
        return self.name

class questionmanager(models.Manager):
    def new_questions(self):
        return self.annotate(answers_amount=Count('answers')).order_by('-id')

    def hot_questions(self):
        return self.annotate(answers_amount=Count('answers')).order_by('-rating')

    def tagged_questions(self, tag_name):
        return self.filter(tags__name=tag_name).annotate(answers_amount=Count('answers')).order_by('-id')

class question(models.Model):
    title = models.CharField(("title"), max_length=254)
    text = models.TextField(("text"))
    author = models.ForeignKey(profile, verbose_name=("author"), on_delete=models.CASCADE)
    date = models.DateField(("date"), auto_now=False, auto_now_add=True)
    tags = models.ManyToManyField(tag, verbose_name=("tags"))
    rating = models.IntegerField(("rating"))
    objects = questionmanager()
    class Meta:
        verbose_name = ("question")
        verbose_name_plural = ("questions")

    def __str__(self):
        return self.title
    
class answermanager(models.Manager):
    def question_answers(self, question_id):
        return self.filter(answered_question=question_id).order_by('id')

class answer(models.Model):
    answered_question = models.ForeignKey(question, verbose_name=("question"), related_name=("answers"), on_delete=models.CASCADE) 
    text = models.TextField(("text"))
    author = models.ForeignKey(profile, verbose_name=("author"), on_delete=models.CASCADE)
    date = models.DateField(("date"), auto_now=False, auto_now_add=True)
    flag = models.BooleanField(("flag"))
    rating = models.IntegerField(("rating"))
    objects = answermanager()
    class Meta:
        verbose_name = ("answer")
        verbose_name_plural = ("answers")
    def __str__(self):
        return self.name

class questionlike(models.Model):
    VALUE_CHOICES = (
        (1, "like"),
        (-1, "dislike")
    )
    value = models.IntegerField("value", choices=VALUE_CHOICES)
    question = models.ForeignKey(question, verbose_name="question", on_delete=models.CASCADE)
    profile = models.ForeignKey(profile, verbose_name="profile", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "questionlike"
        verbose_name_plural = "questionlikes"

    def __str__(self):
        return self.question.title[:30] + "..."


class answerlike(models.Model):
    VALUE_CHOICES = (
        (1, "like"),
        (-1, "dislike")
    )
    value = models.IntegerField("value", choices=VALUE_CHOICES)
    answer = models.ForeignKey(answer, verbose_name="answer", on_delete=models.CASCADE)
    profile = models.ForeignKey(profile, verbose_name="profile", on_delete=models.CASCADE)
    

    class Meta:
        verbose_name = "answerlike"
        verbose_name_plural = "answerlikes"

    def __str__(self):
        return self.answer.title[:30] + "..."
    

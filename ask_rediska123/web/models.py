from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count, Sum
from django.db.models.functions import Coalesce

class profile(models.Model):
    user = models.OneToOneField(User, verbose_name=("user"), on_delete=models.CASCADE)
    avatar = models.ImageField(("avatar"), upload_to="uploads", height_field=None, width_field=None, max_length=None)
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
        return self.annotate().order_by('-id')

    def hot_questions(self):
        return self.annotate(rating=Coalesce(Sum("questionlike__value"), 0)).order_by('-rating')

    def tagged_questions(self, tag_name):
        return self.filter(tags__name=tag_name).annotate(answers_amount=Count('answers')).order_by('-id')

class question(models.Model):
    title = models.CharField(("title"), max_length=254)
    text = models.TextField(("text"))
    author = models.ForeignKey(profile, verbose_name=("author"), on_delete=models.CASCADE)
    date = models.DateField(("date"), auto_now=False, auto_now_add=True)
    tags = models.ManyToManyField(tag, verbose_name=("tags"))
    objects = questionmanager()
    
    def rating(self):
        return self.questionlike_set.aggregate(rating=models.Sum('value'))['rating'] or 0
    
    def answers_amount(self):
        return answer.objects.filter(answered_question=self).count()
    
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
    flag = models.BooleanField(("flag"), default=False)
    objects = answermanager()
    
    def rating(self):
        return self.answerlike_set.aggregate(rating=models.Sum('value'))['rating'] or 0
    
    class Meta:
        verbose_name = ("answer")
        verbose_name_plural = ("answers")
    def __str__(self):
        return self.text[:30] + "..."

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
        unique_together = [["question", "profile"]]

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
        unique_together = [["answer", "profile"]]

    def __str__(self):
        return self.answer.text[:30] + "..."
    

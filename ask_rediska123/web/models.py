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

class questionlikemanager(models.Manager):
    def like_dislike(self, question_id, user, value):
        author = profile.objects.get(user=user)
        liked_question = question.objects.get(id=question_id)
        like, created_flag = questionlike.objects.get_or_create(liked_question=liked_question, author=author)
        if like.value == 1 and value == -1: # Если был лайк и нажали дизлайк (отмена лайка)
            like.value = 0
        elif like.value == -1 and value == 1: # Если был дизлайк и нажали лайк (отмена дизлайка)
            like.value = 0
        elif like.value == 0: # Если было без оценки, то оцениваем
            like.value = value
        like.save()
        return liked_question.rating()

class questionlike(models.Model):
    VALUE_CHOICES = (
        (1, "like"),
        (-1, "dislike")
    )
    value = models.IntegerField("value", choices=VALUE_CHOICES, default=1)
    liked_question = models.ForeignKey(question, verbose_name="question", on_delete=models.CASCADE)
    author = models.ForeignKey(profile, verbose_name="profile", on_delete=models.CASCADE)
    objects = questionlikemanager()

    class Meta:
        verbose_name = "questionlike"
        verbose_name_plural = "questionlikes"
        unique_together = [["liked_question", "author"]]

    def __str__(self):
        return self.liked_question.title[:30] + "..."
    
class answermanager(models.Manager):
    def question_answers(self, question_id):
        return self.filter(answered_question=question_id).order_by('id')
    
    def correct(self, user, answer_id):
        answer = self.get(id=answer_id)
        question_author = answer.answered_question.author.user
        if user == question_author: # Если нажимает авто вопроса
            answer.flag = not answer.flag
            answer.save()
            #print(answer.flag) # Для отладки

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

class answerlikemanager(models.Manager):
    def like_dislike(self, answer_id, user, value):
        author = profile.objects.get(user=user)
        liked_answer = answer.objects.get(id=answer_id)
        like, created_flag = answerlike.objects.get_or_create(liked_answer=liked_answer, author=author)
        if like.value == 1 and value == -1: # Если был лайк и нажали дизлайк (отмена лайка)
            like.value = 0
        elif like.value == -1 and value == 1: # Если был дизлайк и нажали лайк (отмена дизлайка)
            like.value = 0
        elif like.value == 0: # Если было без оценки, то оцениваем
            like.value = value
        like.save()
        return liked_answer.rating()

class answerlike(models.Model):
    VALUE_CHOICES = (
        (1, "like"),
        (-1, "dislike")
    )
    value = models.IntegerField("value", choices=VALUE_CHOICES, default=1)
    liked_answer = models.ForeignKey(answer, verbose_name="answer", on_delete=models.CASCADE)
    author = models.ForeignKey(profile, verbose_name="profile", on_delete=models.CASCADE)
    objects = answerlikemanager()

    class Meta:
        verbose_name = "answerlike"
        verbose_name_plural = "answerlikes"
        unique_together = [["liked_answer", "author"]]

    def __str__(self):
        return self.answer.text[:30] + "..."
    

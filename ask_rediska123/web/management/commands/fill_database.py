import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from web.models import *
from faker import Faker

fake = Faker()

class Command(BaseCommand):
    help = 'Fill the database with test data'

    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int)

    def handle(self, *args, **kwargs):
        ratio = kwargs['ratio']
        
        # Создание пользователей
        if User.objects.count() < 10000:
            if User.objects.count() < 100:
                users_list = [
                    User(
                        username=f'user{i}',
                        email=f'user{i}@example.com',
                        password=make_password('password')
                    ) for i in range(100)]
            else:
                users_list = list()
            user_len = int(User.objects.count())
            for i in range(user_len, ratio):
                User.objects.create(
                    username=f'user{i}',
                    email=f'user{i}@example.com',
                    password='password'
                )

        users_list = User.objects.filter()
        self.stdout.write(self.style.SUCCESS('filled users'))
        
        # Создание профилей (на основе пользователей)
        if profile.objects.count() < 10000:
            profiles_list = [
                profile(
                    user=users_list[i],
                    avatar = f'avatar_{i}.png',
                    rating=random.randint(1, 100))
                for i in range(ratio)]
            profile.objects.bulk_create(profiles_list)
        else:
            profiles_list = list(profile.objects.filter())
        self.stdout.write(self.style.SUCCESS('filled profiles'))

        # Создание тегов
        if tag.objects.count() < 10000:
            tags_list = [tag(name=fake.sentence(nb_words=1)) for i in range(ratio)]
            tag.objects.bulk_create(tags_list)
        else:
            tags_list = list(tag.objects.filter())
        self.stdout.write(self.style.SUCCESS('filled tags'))

        # Создание вопросов
        if question.objects.count() < 100_000:
            questions_list = [
                question(
                    title=fake.text(max_nb_chars=120),
                    text=fake.text(max_nb_chars=500),
                    author=random.choice(profiles_list),
                    rating=random.randint(1, 100))
                for i in range(ratio * 10)]
            question.objects.bulk_create(questions_list)
            for i in questions_list:
                question_tags_list = list({random.choice(tags_list) for j in range(random.randint(1,10))})
                for j in question_tags_list:
                    i.tags.add(j)
        else:
            questions_list = list(question.objects.filter())
            
        self.stdout.write(self.style.SUCCESS('filled questions')) 
        
        # Создание ответов
        if answer.objects.count() < 1_000_000:
            answers_list = [
                answer(
                    answered_question=random.choice(questions_list),
                    text=fake.text(max_nb_chars=500),
                    author=random.choice(profiles_list),
                    flag=random.choice([True, False]),
                    rating=random.randint(1, 100))
                for i in range(ratio * 100)]
            answer.objects.bulk_create(answers_list)
        else:
            answers_list = list(answer.objects.filter())
        self.stdout.write(self.style.SUCCESS('filled answers'))
        
        # Создание лайков/дизлайков на вопросы
        if questionlike.objects.count() < 100_000:
            questionlikes_list = [
                questionlike(
                    value=random.randint(1, 2),
                    profile=random.choice(profiles_list),
                    question=random.choice(questions_list)
                )
                for i in range(ratio * 20)
            ]
            questionlike.objects.bulk_create(questionlikes_list)
        else:
            questionlikes_list = list(questionlike.objects.filter())
        self.stdout.write(self.style.SUCCESS('filled questionlikes'))
        
        # Создание лайков/дизлайков на ответы
        if answerlike.objects.count() < 1_000_000:
            answerlikes_list = [
                answerlike(
                    value=random.randint(1, 2), 
                    profile=random.choice(profiles_list),
                    answer=random.choice(answers_list)
                )
                for i in range(ratio * 180)
            ]
            answerlike.objects.bulk_create(answerlikes_list)
        else:
            answerlikes_list = list(answerlike.objects.filter())
        self.stdout.write(self.style.SUCCESS('filled answerlikes'))  
            
        self.stdout.write(self.style.SUCCESS('Successfully filled the database with test data'))
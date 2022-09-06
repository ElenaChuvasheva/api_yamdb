from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


#class Review(models.Model):
#    text = models.TextField(verbose_name='Текст отзыва')
#    pub_date = models.DateTimeField(verbose_name='Дата публикации')    
#    pub_date = models.DateTimeField(auto_now_add=True,
#                                    verbose_name='Дата публикации')
#    author = models.ForeignKey(User, on_delete=models.CASCADE,
#                               related_name='posts',
#                               verbose_name='Автор')

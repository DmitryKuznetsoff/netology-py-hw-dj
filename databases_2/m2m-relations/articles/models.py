from django.db import models


class Article(models.Model):
    title = models.CharField(max_length=256, unique=True, verbose_name='Название')
    text = models.TextField(unique=True, verbose_name='Текст')
    published_at = models.DateTimeField(verbose_name='Дата публикации')
    image = models.ImageField(null=True, blank=True, verbose_name='Изображение', )
    groups = models.ManyToManyField('Group', through='GroupArticle')

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

    def __str__(self):
        return self.title


class Group(models.Model):
    title = models.CharField(max_length=256, unique=True, verbose_name='Название')

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Гпуппы'

    def __str__(self):
        return self.title


class GroupArticle(models.Model):
    article = models.ForeignKey(Article, related_name='groups_in_article', on_delete=models.DO_NOTHING)
    groups = models.ForeignKey(Group, related_name='groups', on_delete=models.DO_NOTHING)
    is_main = models.BooleanField()

    class Meta:
        db_table = 'articles_group_article'
        ordering = ['-is_main', 'groups__title']

    def __str__(self):
        return f'{self.groups.title}'

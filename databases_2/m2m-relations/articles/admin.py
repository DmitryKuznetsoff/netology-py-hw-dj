from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from .models import Article, Group, GroupArticle


class GroupArticleInlineFormset(BaseInlineFormSet):
    def clean(self):
        article_title = self.cleaned_data[0].get('article')
        # Если у текущей статьи уже есть группы и пользователь решил их поменять:
        if article_title:
            article = Article.objects.prefetch_related().get(title=article_title)

            # Названия закреплённых за статьёй групп:
            groups = [{'group': group['title']} for group in article.groups.values()]
            # Признак 'is_main' закреплённых за статьёй групп:
            main = [{'is_main': group['is_main']} for group in article.groups_in_article.values()]

            # Формируем список словарей использующихся в статье групп:
            existing_groups = [{**s, **m, 'DELETE': False} for s, m in zip(groups, main)]
        # Если у текущей статьи нет групп и пользователь решил впервые их установить:
        else:
            existing_groups = []

        for form in self.forms:
            try:
                group = str(form.cleaned_data['groups'])
                is_main = form.cleaned_data['is_main']
                delete = form.cleaned_data['DELETE']

                new_group = {'group': group, 'is_main': is_main, 'DELETE': delete}
            except KeyError:
                new_group = {}

            # Если такой группы ещё нет - добавляем словарь в existing_groups:
            if new_group.get('group') not in [group.get('group') for group in existing_groups]:
                existing_groups.append(new_group)
            # Если такая группа есть в existing_groups - обновляем значения на новые:
            else:
                [group.update(new_group) for group in existing_groups if new_group.get('title') == group.get('title')]

        # Убираем из списка "пустые" группы если они есть:
        existing_groups = [group for group in existing_groups if group]

        # Из existing_groups выбираем группы с признаком 'is_main' и без признака 'DELETE':
        check = [group.get('is_main') for group in existing_groups if
                 group.get('is_main') and not group.get('DELETE')]

        if not check:
            raise ValidationError('Одна из групп должна быть отмечена как основная')
        elif len(check) > 1:
            raise ValidationError('Основной может быть только одна группа')
        else:
            return super().clean()


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    pass


class GroupArticleInline(admin.TabularInline):
    model = GroupArticle
    extra = 3
    formset = GroupArticleInlineFormset


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [GroupArticleInline]

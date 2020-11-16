from django.contrib.auth.models import User
from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from advertisements.models import Advertisement, Favorites


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name',)


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""

    creator = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator',
                  'status', 'created_at',)

    def create(self, validated_data):
        """Метод для создания"""

        # Простановка значения поля создатель по-умолчанию.
        # Текущий пользователь является создателем объявления
        # изменить или переопределить его через API нельзя.
        # обратите внимание на `context` – он выставляется автоматически
        # через методы ViewSet.
        # само поле при этом объявляется как `read_only=True`
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        """Метод для валидации. Вызывается при создании и обновлении."""
        user = self.context['request'].user
        ads = Advertisement.objects.select_related().filter(creator__username=user, status='OPEN')
        if len(ads) == 10:
            raise ValidationError({'error': 'Может быть не более 10 открытых объявлений'})

        return data


class FavoritesSerializer(serializers.ModelSerializer):

    class Meta:

        model = Favorites
        fields = ('advertisement',)

    def validate(self, attrs):
        if self.context['request'].user == attrs['advertisement'].creator:
            raise ValidationError({'error': 'Нельзя добавлять в избранные собственные объявления'})

        if attrs['advertisement'].status == 'DRAFT':
            raise ValidationError({'error': 'Нельзя добавить в избранное объявление со статусом "Черновик"'})

        existing_fav = Favorites.objects.filter(user=self.context['request'].user)
        if attrs['advertisement'] in [fav.advertisement for fav in existing_fav]:
            raise ValidationError({'error': 'Данное объявление уже есть в избранном'})
        return attrs

    def create(self, validated_data):
        validated_data['user_id'] = self.context['request'].user.id
        return super().create(validated_data)

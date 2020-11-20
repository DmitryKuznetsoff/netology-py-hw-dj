from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import ObjectDoesNotExist
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from api.models import Product, Review, Order, Collection, ProductOrderPosition


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для пользователей
    """

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name',)


class ProductSerializer(serializers.ModelSerializer):
    """
    Сериализатор для товаров
    """

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'created_at', 'updated_at']


class ProductOrderPositionSerializer(serializers.Serializer):
    """
    Сериализатоор для вложенного поля 'positions' в OrderSerializer
    """
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(),
                                                    source='product.id')
    name = serializers.CharField(source='product.name', read_only=True)
    amount = serializers.IntegerField(min_value=1)


class ProductCollectionSerializer(serializers.Serializer):
    """
    Сериализатор для вложенного поля 'products' в CollectionSerializer
    """
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    name = serializers.CharField(source='product.name', read_only=True)
    price = serializers.CharField(source='product.price', read_only=True)


class ReviewSerializer(serializers.ModelSerializer):
    """
    Сериализатор для отзывов
    """
    user = serializers.IntegerField(read_only=True, source='user.id')

    class Meta:
        model = Review
        fields = ['id', 'user', 'product', 'text', 'rating']

    def validate(self, attrs):
        if self.context['view'].action == 'create':
            user = self.context['request'].user
            product = attrs['product']
            existing_review = Review.objects.filter(user=user, product=product)
            if existing_review:
                raise ValidationError({'error': 'К товару можно оставлять только 1 отзыв'})
            attrs['user'] = user
        elif self.context['view'].action in ['update', 'partial_update']:
            # Поля, которые пользователь может изменить через patch-запрос:
            allowed_fields = {'rating', 'text'}
            if attrs.keys() - allowed_fields:
                raise ValidationError({'error': f'Допустимые поля для изменения: {", ".join(sorted(allowed_fields))}'})

        return attrs

    @transaction.atomic
    def create(self, validated_data):
        return super().create(validated_data)


class OrderSerializer(serializers.ModelSerializer):
    """
    Сериализатор для заказов
    """
    positions = ProductOrderPositionSerializer(many=True, required=True)

    class Meta:
        model = Order
        fields = ('id', 'user', 'positions', 'status', 'order_sum', 'created_at', 'updated_at')
        read_only_fields = ['user']

    def validate(self, attrs):
        user = self.context['request'].user
        if self.context['view'].action == 'create':
            positions = attrs.get('positions')
            # Проверка создания заказа с пустым списком товаров:
            if not positions:
                raise ValidationError({'positions': 'Не указан список товаров'})
            # Проверка на уникальность продуктов в заказе:
            products_ids_set = {position['product']['id'].id for position in positions}
            if len(products_ids_set) != len(positions):
                raise ValidationError({'positions': 'В заказе содержатся дубли'})

            price = (position['product']['id'].price for position in positions)
            amount = (position['amount'] for position in positions)
            order_sum = round(sum(price * amount for price, amount in zip(price, amount)), 2)

            attrs['user'] = user
            attrs['order_sum'] = order_sum

        elif self.context['view'].action in ['update', 'partial_update']:
            # Поля, которые пользователь может изменить через patch-запрос:
            allowed_fields = {'positions'}
            # Если пользователь админ - добавляем поле 'status' к allowed_fields
            allowed_fields.add('status') if user.is_staff else allowed_fields
            if attrs.keys() - allowed_fields:
                raise ValidationError({'error': f'Допустимые поля для изменения: {", ".join(sorted(allowed_fields))}'})

        return attrs

    @transaction.atomic
    def create(self, validated_data):
        positions = validated_data.pop('positions')
        order = super().create(validated_data)

        positions_objs = [
            ProductOrderPosition(
                amount=position['amount'],
                product=position['product']['id'],
                order=order
            )
            for position in positions
        ]

        ProductOrderPosition.objects.bulk_create(positions_objs)
        return order

    @transaction.atomic
    def update(self, instance, validated_data):
        positions = validated_data.get('positions')
        # Обработка вложенного поля 'positions':
        for position in positions:
            if positions:
                product_id = position['product']['id'].id
                amount = position['amount']
                try:
                    position_obj = ProductOrderPosition.objects.get(product_id=product_id, order=instance)
                    position_obj.amount = amount
                    position_obj.save()
                except ObjectDoesNotExist:
                    ProductOrderPosition.objects.create(product_id=product_id, amount=amount, order=instance)
        validated_data.pop('positions')

        # TODO: сделать, чтобы оно работало:
        # После обновления списка позиций перерсчитываем сумму заказа:
        order_sum = round(sum(position.product.price * position.amount for position in instance.positions.all()), 2)

        validated_data['order_sum'] = order_sum
        instance = super().update(instance, validated_data)

        return instance


class CollectionSerializer(serializers.ModelSerializer):
    """
    Сериализатор для подборок товаров
    """
    products_list = ProductCollectionSerializer(many=True, required=True)

    class Meta:
        model = Collection
        fields = ['title', 'text', 'products_list', 'created_at', 'updated_at']

    def validate(self, attrs):
        products_list = attrs.get('products_list')
        if self.context['view'].action == 'create':
            # Проверка создания подборки с пустым списком товаров:
            if not products_list:
                raise ValidationError({'products': 'Не указан список товаров'})

            # Проверка на уникальность товаров в подборке:
            products_ids_set = {product['product_id'].id for product in products_list}
            if len(products_ids_set) != len(products_list):
                raise ValidationError({'products': 'В подборке содержатся дубли'})

        return attrs

    @transaction.atomic
    def create(self, validated_data):
        products_list = validated_data.pop('products_list')
        collection = super().create(validated_data)

        products_objs = [Product.objects.get(id=product['product_id'].id) for product in products_list]
        collection.products.add(*products_objs)

        return collection

    @transaction.atomic
    def update(self, instance, validated_data):
        products_list = validated_data.get('products_list')
        # Обработка вложенного поля 'products_list':
        if products_list:
            # Из переданных товаров выбираем те, которых ещё нет в коллекции:
            existing_products = instance.products.all()
            new_products = [product['product_id'] for product in products_list if
                            product['product_id'] not in existing_products]
            # Добавляем новые товары в инстанс коллекции если они есть:
            if new_products:
                instance.products.add(*new_products)
            validated_data.pop('products_list')

        # Обработка невложенных полей:
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance

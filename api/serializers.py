from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from recipes.models import Ingredient, Recipe, User

from .models import Favorite, Purchase, Subscribe


class FavoriteSerializer(serializers.ModelSerializer):
    id = serializers.SlugRelatedField(
        slug_field='id', queryset=Recipe.objects.all(), source='recipe')
    user = serializers.PrimaryKeyRelatedField(
        read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        fields = ['id', 'user']
        model = Favorite
        validators = [
            UniqueTogetherValidator(
                queryset=Favorite.objects.all(),
                fields=['id', 'user']
            )
        ]

    def create(self, validated_data):
        if 'user' not in validated_data:
            validated_data['user'] = self.context['request'].user
        return Favorite.objects.create(**validated_data)


class PurchaseSerializer(serializers.ModelSerializer):
    id = serializers.SlugRelatedField(slug_field='id',
                                      queryset=Recipe.objects.all(),
                                      source='recipe')
    serializer_user = serializers.CurrentUserDefault()
    user = serializers.PrimaryKeyRelatedField(read_only=True,
                                              default=serializer_user)

    class Meta:
        fields = ['id', 'user']
        model = Purchase
        validators = [
            UniqueTogetherValidator(
                queryset=Purchase.objects.all(),
                fields=['id', 'user']
            )
        ]

    def create(self, validated_data):
        if 'user' not in validated_data:
            validated_data['user'] = self.context['request'].user
        return Purchase.objects.create(**validated_data)


class SubscribeSerializer(serializers.ModelSerializer):
    id = serializers.SlugRelatedField(slug_field='id',
                                      queryset=User.objects.all(),
                                      source='author')
    user = serializers.PrimaryKeyRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault())

    class Meta:
        fields = ['id', 'user']
        model = Subscribe
        validators = [
            UniqueTogetherValidator(
                queryset=Subscribe.objects.all(),
                fields=['id', 'user']
            )
        ]

    def create(self, validated_data):
        if 'user' not in validated_data:
            validated_data['user'] = self.context['request'].user
        return Subscribe.objects.create(**validated_data)


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Ingredient

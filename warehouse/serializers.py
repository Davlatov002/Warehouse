from rest_framework import serializers
from .models import Product, Material, ProductMaterial, Warehouse

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = '__all__'

class ProductMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductMaterial
        fields = '__all__'

class WarehouseSerializer(serializers.ModelSerializer):
    material = serializers.StringRelatedField(source='material.name')
    class Meta:
        model = Warehouse
        fields = '__all__'

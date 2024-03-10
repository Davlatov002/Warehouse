from django.db import models
import uuid

# Mahsulot – ishlab chiqariladigan mahsulotlar
class Product(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    name = models.CharField(max_length=100)
    code = models.IntegerField()

    def __str__(self) -> str:
        return self.name

# Xomashyo – mahsulot ishlab chiqarish uchun foydalaniladigan xomashyolar
class Material(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name

# Mahsulot-Xomashyo (product-materials - yordamchi jadval) – qaysi 
# mahsulotni ishlab chiqarish uchun qanday mahsulotlar ishlatilinishini ko’rsatadi.
class ProductMaterial(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    products = models.ForeignKey(Product, related_name="Product", on_delete=models.CASCADE)
    material = models.ForeignKey(Material, related_name="material", on_delete=models.CASCADE)
    quantity = models.FloatField()

    def __str__(self) -> str:
        return self.products.name
    
# Omborxona (warehouses) – partiya bo’lib kelgan xomashyolar jamlanmasi.
class Warehouse(models.Model):
    material = models.ForeignKey(Material, related_name="Material", on_delete=models.CASCADE)
    remainder = models.IntegerField()
    price = models.IntegerField()

    def __str__(self) -> str:
        return self.material.name

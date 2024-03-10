from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Product, Material, ProductMaterial, Warehouse
from drf_yasg.utils import swagger_auto_schema
from .serializers import ProductSerializer, ProductMaterialSerializer, MaterialSerializer, WarehouseSerializer
from django.shortcuts import render



@swagger_auto_schema(methods='GET')
@api_view(['GET'])
def get_warehous(request):
    if request.method == 'GET':
        warehouse = Warehouse.objects.all()
        serializer = WarehouseSerializer(warehouse, many=True)
        return Response({"Warehouse":serializer.data}, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(methods='GET')
@api_view(['GET'])
def get_materials(request):
    if request.method == 'GET':
        materials = Material.objects.all()
        serializer = MaterialSerializer(materials, many=True)
        return Response({"Materials":serializer.data}, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
@swagger_auto_schema(methods='GET')
@api_view(['GET'])
def get_products(request):
    if request.method == 'GET':
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response({"Products":serializer.data}, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    

@swagger_auto_schema(methods='GET')
@api_view(['GET'])
def calculate(request):
    mahsulotlar = []# Mahsulotlar va ularning miqdori
    products = Product.objects.all()     # malumotlar bazasidagi barcha productlarni olish
    productmaterials = ProductMaterial.objects.all()   # malumotlar bazasidagi barcha productmaterialarni olish
    for product in products:
        materials = []   # product ga qanaqa material va qancha miqtorda ketishini shu listga jamlab hisoblab chiqamiz
        for pm in productmaterials:
            if pm.products.name == product.name:
                materials.append({"name":pm.material.name, "qty":pm.quantity*float(product.code)})
        mahsulotlar.append({"name":product.name, "qty": product.code, "materials":materials})
    
    # Omborxonadagi xomashyolar
    warehouses = Warehouse.objects.all()
    
    # “warehouses” jadvaldagi malumotlarni o'zgartirmaslik uchun malumotlarni shu listga jamlaymiz. 
    xomashyolar = []
    for xomashyo in warehouses:
        xomashyolar.append({"id":xomashyo.id,"name":xomashyo.material.name,"remainder": xomashyo.remainder, "price": xomashyo.price})
    
    # Mahsulotlar uchun xomashyolarni hisoblash
    javob = {"result": []}
    for mahsulot in mahsulotlar: # har bir mahsulotni birma bir aylanib chiqadi.
        product_name = mahsulot["name"]
        product_qty = mahsulot["qty"]
        product_materials = []

        for material in mahsulot["materials"]: 
            material_name = material["name"]
            material_qty = material["qty"]
            s = 0 # har bir murojat qilinayotgan xamoshiyo ning indeksini hisoblash uchun
            for warehouse in xomashyolar:
                
                if warehouse["name"] == material_name and material_qty > 0:
                    qty_from_warehouse = warehouse["remainder"]
                    if material_qty <= qty_from_warehouse:
                        price = warehouse["price"]
                        product_materials.append({
                            "warehouse_id": warehouse['id'],
                            "material_name": material_name,
                            "qty": material_qty,
                            "price": price
                        })
                        xomashyolar[s]["remainder"] -= material_qty
                        qty_from_warehouse -= material_qty
                        material_qty = 0
                        s += 1
                        continue 
                    elif qty_from_warehouse > 0:
                        price = warehouse["price"]
                        product_materials.append({
                            "warehouse_id": warehouse["id"],
                            "material_name": material_name,
                            "qty": qty_from_warehouse,
                            "price": price
                        })
                        
                        material_qty -= qty_from_warehouse
                        xomashyolar[s]["remainder"]=0
                        qty_from_warehouse = 0
                s += 1
                
            if  material_qty > 0:
                product_materials.append({
                    "warehouse_id": None,
                    "material_name": material_name,
                    "qty": material_qty,
                    "price": None
                })

        javob["result"].append({
            "product_name": product_name,
            "product_qty": product_qty,
            "product_materials": product_materials
        })

    return Response(javob)




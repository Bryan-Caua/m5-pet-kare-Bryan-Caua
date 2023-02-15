from rest_framework.views import APIView, Request, Response, status
from .models import Pet
from .serializers import PetSerializer
from django.shortcuts import get_object_or_404
from groups.models import Group
from traits.models import Trait
from rest_framework.pagination import PageNumberPagination

class PetsViews(APIView, PageNumberPagination):
    def get(self, request: Request):
        trait = request.query_params.get("trait")
        if trait:
            pets = Pet.objects.filter(traits__name = trait)
        else:
            pets = Pet.objects.all()
        result_page = self.paginate_queryset(pets, request)
        serializer = PetSerializer(result_page, many=True)
        return self.get_paginated_response(serializer.data)

    def post(self, request: Request):
        serializer = PetSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        group_data = serializer.validated_data.pop("group")
        traits_list = serializer.validated_data.pop("traits")
        try:
            group = Group.objects.get(scientific_name=group_data["scientific_name"])
        except Group.DoesNotExist:    
            group = Group.objects.create(**group_data)
        pet = Pet.objects.create(**serializer.validated_data, group=group)
        for trait_data in traits_list:
            try:
                trait = Trait.objects.get(name__iexact=trait_data["name"])
            except Trait.DoesNotExist:    
                trait = Trait.objects.create(**trait_data)
            pet.traits.add(trait)
        serializer = PetSerializer(pet)
        return Response(serializer.data, status.HTTP_201_CREATED)

class PetsDatailView(APIView):
    def get(self, request: Request, pet_id):
        petValidate = get_object_or_404(Pet, id=pet_id)
        serializer = PetSerializer(petValidate)
        return Response(serializer.data)

    
    def patch(self, request: Request, pet_id: int):
        petValidate = get_object_or_404(Pet, id=pet_id)
        serializer = PetSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        group_dic = serializer.validated_data.pop("group", None)
        trait_list = serializer.validated_data.pop("traits", None)
        if group_dic:
            try:
                group_obj = Group.objects.get(scientific_name = group_dic["scientific_name"]) 
            except Group.DoesNotExist: 
                group_obj = Group.objects.create(**group_dic)
            petValidate.group = group_obj     
        
        if trait_list:
            trait_new_list = []
            for obj in trait_list:
                try:
                    trait = Trait.objects.get(name__iexact = obj["name"])
                except Trait.DoesNotExist:
                    trait = Trait.objects.create(**obj)
                trait_new_list.append(trait)
            petValidate.traits.set(trait_new_list)    
        
        for key, value in serializer.validated_data.items():
            setattr(petValidate, key, value)
        petValidate.save()

        serializer = PetSerializer(petValidate)

        return Response(serializer.data, status.HTTP_200_OK)
    
    def delete(self, request: Request, pet_id: int) -> Response:
        pet = get_object_or_404(Pet, id=pet_id)
        pet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

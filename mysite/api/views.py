from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
from django.views import View
from .models import Recipe
import json
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


@method_decorator(csrf_exempt, name='dispatch')
class recipeView(View):
    # Get all recipes
    def get(self, request):
        entries = Recipe.objects.all()
        entries_list = list(entries.values('id', 'title', 'ingredients', 'instructions', 'cuisine'))
        return JsonResponse(entries_list, safe=False, status = 200)
    
    def post(self, request):
        try:
            data = json.loads(request.body)
            title = data.get('title')
            ingredients = data.get('ingredients')
            instructions = data.get('instructions')
            cuisine = data.get('cuisine')
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON format'}, status = 400)
        
        if not title or not ingredients or not instructions or not cuisine:
            return JsonResponse({'message': 'Missing required fields'}, status = 400)
        
        entry = Recipe(title = title, ingredients = ingredients, instructions = instructions, cuisine = cuisine)
        entry.save()

        return JsonResponse({'id': entry.id, 'title': entry.title, 'ingredients': entry.ingredients, 'instructions': entry.instructions, 'cuisine': entry.cuisine}, status = 201)
    

@method_decorator(csrf_exempt, name='dispatch')
class recipeViewById(View):
    # Get recipe by id
    def get(self, request, id):
        try:
            entry = Recipe.objects.get(id = id)
        except Recipe.DoesNotExist:
            return JsonResponse({'message': 'Recipe not found'}, status = 404)
        
        return JsonResponse({'id': entry.id, 'title': entry.title, 'ingredients': entry.ingredients, 'instructions': entry.instructions, 'cuisine': entry.cuisine}, status = 200)

    def delete(self, request, id):
        try:
            entry = Recipe.objects.get(id = id)
        except Recipe.DoesNotExist:
            return JsonResponse({'message': 'Recipe not found'}, status = 404)
        
        entry.delete()
        return JsonResponse({'message': 'Recipe deleted successfully'}, status = 204)
    
    def put(self, request, id):
        try:
            entry = Recipe.objects.get(id = id)
        except Recipe.DoesNotExist:
            return JsonResponse({'message': 'Recipe not found'}, status = 404)
        
        try:
            data = json.loads(request.body)
            title = data.get('title', None)
            ingredients = data.get('ingredients', None)
            instructions = data.get('instructions', None)
            cuisine = data.get('cuisine', None)
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON format'}, status = 400)
        
        if not title and not ingredients and not instructions and not cuisine:
            return JsonResponse({'message': 'At least one field is request for update'}, status = 400)
        
        # in put request partial data is accepted we only update that fields which are provided in request
        if title:
            entry.title = title
        if ingredients:
            entry.ingredients = ingredients
        if instructions:
            entry.instructions = instructions
        if cuisine:
            entry.cuisine = cuisine
        
        entry.save()

        return JsonResponse({'id': entry.id, 'title': entry.title, 'ingredients': entry.ingredients, 'instructions': entry.instructions, 'cuisine': entry.cuisine}, status = 200)
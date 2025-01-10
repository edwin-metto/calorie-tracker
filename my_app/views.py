from django.shortcuts import render, redirect, get_object_or_404
from .models import FoodItem
from .forms import FoodItemForm
from django.utils import timezone
from django.db.models import Sum

def home(request):
    today = timezone.now().date()
    food_items = FoodItem.objects.filter(date_added=today)
    total_calories = food_items.aggregate(Sum('calories'))['calories__sum'] or 0
    context = {
        'food_items': food_items,
        'total_calories': total_calories,
        'form': FoodItemForm(),
    }
    return render(request, 'my_app/home.html', context)

def add_food(request):
    if request.method == 'POST':
        form = FoodItemForm(request.POST)
        if form.is_valid():
            food = form.save(commit=False)
            food.date_added = timezone.now().date()
            food.save()
    return redirect('home')

def delete_food(request, pk):
    food = get_object_or_404(FoodItem, pk=pk)
    if food.date_added == timezone.now().date():
        food.delete()
    return redirect('home')

def reset_calories(request):
    today = timezone.now().date()
    FoodItem.objects.filter(date_added=today).delete()
    return redirect('home')


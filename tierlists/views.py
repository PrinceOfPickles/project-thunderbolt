from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .models import TierList, TierListItem
from reviews.models import EnergyDrink
from .forms import TierListForm
from django.db.models import Q
import json

def tierlists(request):
    tierlists = TierList.objects.filter(is_hidden=False)
    return render(request, 'tierlists/tierlists.html', {'tierlists': tierlists})

def tierlist_detail(request, tierlist_id):
    tierlist = get_object_or_404(TierList, id=tierlist_id)
    items = TierListItem.objects.filter(tier_list=tierlist)
    
    tier_order = ['S-Tier', 'A-Tier', 'B-Tier', 'C-Tier', 'D-Tier', 'F-Tier']

    tier_data = []
    for tier_name in tier_order:
        tier_items = [item for item in items if item.tier == tier_name]
        tier_data.append({
            'name': tier_name,
            'items': tier_items
        })

    is_owner = request.user == tierlist.user

    return render(request, 'tierlists/tierlist_detail.html', {
        'tierlist': tierlist,
        'tier_data': tier_data,
        'items': items,
        'isOwner': is_owner,
    })

@login_required
def create_tierlist(request):
    if request.method == 'POST':
        form = TierListForm(request.POST)
        if form.is_valid():
            tierlist = form.save(commit=False)
            tierlist.user = request.user
            tierlist.save()
            return redirect('add_drinks_to_tierlist', tierlist_id=tierlist.id)
    else:
        form = TierListForm()
    return render(request, 'tierlists/create_tierlist.html', {'form': form})

@login_required
def edit_tierlist(request, tierlist_id):
    tierlist = get_object_or_404(TierList, id=tierlist_id)
    if request.user != tierlist.user:
        return redirect('tierlists')
    if request.method == 'POST':
        form = TierListForm(request.POST, instance=tierlist)
        if form.is_valid():
            form.save()
            return redirect('tierlist_detail', tierlist_id=tierlist.id)
    else:
        form = TierListForm(instance=tierlist)
    return render(request, 'tierlists/edit_tierlist.html', {'form': form, 'tierlist': tierlist})

@login_required
def delete_tierlist(request, tierlist_id):
    tierlist = get_object_or_404(TierList, id=tierlist_id)
    if request.user != tierlist.user:
        return redirect('tierlists')
    if request.method == 'POST':
        tierlist.delete()
        return redirect('tierlists')
    return render(request, 'tierlists/delete_tierlist.html', {'tierlist': tierlist})

@require_POST
@csrf_exempt
def update_tier(request, item_id):
    try:
        item = TierListItem.objects.get(id=item_id)
        data = json.loads(request.body)
        new_tier = data.get('tier')

        if request.user == item.tier_list.user:
            item.tier = new_tier
            item.save()
            return JsonResponse({'status': 'success', 'message': 'Tier updated successfully'})
        else:
            return JsonResponse({'status': 'error', 'message': 'You do not have permission to update this tier list'}, status=403)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
        
@login_required
def create_tierlist(request):
    if request.method == 'POST':
        form = TierListForm(request.POST)
        if form.is_valid():
            tierlist = form.save(commit=False)
            tierlist.user = request.user
            tierlist.save()
            return redirect('tierlist_detail', tierlist_id=tierlist.id)
    else:
        form = TierListForm()
    return render(request, 'tierlists/create_tierlist.html', {'form': form})

@login_required
def add_drinks_to_tierlist(request, tierlist_id):
    tierlist = get_object_or_404(TierList, id=tierlist_id)
    if request.user != tierlist.user:
        return redirect('tierlists')

    drinks = EnergyDrink.objects.all()

    if request.method == 'POST':
        drink_id = request.POST.get('drink_id')
        tier = request.POST.get('tier')
        if drink_id and tier:
            drink = get_object_or_404(EnergyDrink, id=drink_id)
            # Check if the drink is already in the tier list
            if not TierListItem.objects.filter(tier_list=tierlist, drink=drink).exists():
                TierListItem.objects.create(tier_list=tierlist, drink=drink, tier=tier, position=1)
            return redirect('add_drinks_to_tierlist', tierlist_id=tierlist.id)

    return render(request, 'tierlists/add_drinks_to_tierlist.html', {
        'tierlist': tierlist,
        'drinks': drinks,
    })

def search_drinks(request):
    query = request.GET.get('q', '')
    drinks = EnergyDrink.objects.filter(
        Q(name__icontains=query) |
        Q(brand__icontains=query) |
        Q(series__icontains=query)
    ).values('id', 'name', 'brand')[:10]  # Limit to 10 results
    return JsonResponse(list(drinks), safe=False)

@require_POST
@csrf_exempt
def save_order(request, tierlist_id):
    try:
        tierlist = get_object_or_404(TierList, id=tierlist_id)
        if request.user != tierlist.user:
            return JsonResponse({'status': 'error', 'message': 'You do not have permission to update this tier list'}, status=403)

        data = json.loads(request.body)
        for tier, itemIds in data.items():
            for position, itemId in enumerate(itemIds, start=1):
                item = get_object_or_404(TierListItem, id=itemId)
                item.position = position
                item.save()

        return JsonResponse({'status': 'success', 'message': 'Order saved successfully'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
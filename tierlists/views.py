from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from .models import TierList, TierListItem
from .forms import TierListForm

# class TierListListView(ListView):
#     model = TierList
#     template_name = 'tierlists/tierlist_list.html'
#     context_object_name = 'tierlists'

#     def get_queryset(self):
#         return TierList.objects.filter(is_hidden=False)

def tierlist_detail(request, tierlist_id):
    tierlist = get_object_or_404(TierList, id=tierlist_id)
    items = TierListItem.objects.filter(tier_list=tierlist)
    return render(request, 'tierlists/tierlist_detail.html', {'tierlist': tierlist, 'items': items})

@login_required
def create_tierlist(request):
    if request.method == 'POST':
        form = TierListForm(request.POST)
        if form.is_valid():
            tierlist = form.save(commit=False)
            tierlist.user = request.user
            tierlist.save()
            return redirect('tierlists/tierlist_detail', tierlist_id=tierlist.id)
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
            return redirect('tierlists/tierlist_detail', tierlist_id=tierlist.id)
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
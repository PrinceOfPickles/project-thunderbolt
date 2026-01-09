from django.shortcuts import render
from django.views.generic import ListView
from .models import TierList, TierListItem

class TierListListView(ListView):
    model = TierList
    template_name = 'tierlists/tierlist_list.html'
    context_object_name = 'tierlists'

    def get_queryset(self):
        return TierList.objects.filter(is_hidden=False)

def tierlist_detail(request, tierlist_id):
    tierlist = get_object_or_404(TierList, id=tierlist_id)
    items = TierListItem.objects.filter(tier_list=tierlist)
    return render(request, 'tierlists/tierlist_detail.html', {'tierlist': tierlist, 'items': items})

# Create your views here.

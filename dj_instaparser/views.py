import json
from decimal import Decimal

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.generic.base import View

from dj_instaparser.helpers import validate_hashtag, get_store_items
from dj_instaparser.models import Item


class Main(View):
    def get(self, request):
        return render(request, "main.html")


class CollectItems(View):
    def post(self, request):
        data = request.POST
        account = data.get('account')
        sale_hashtag = data.get('sale_hashtag')
        # remove_hashtags = True if data.get('description_without_hashtags') else False
        if sale_hashtag:
            try:
                validate_hashtag(sale_hashtag)
            except AssertionError as e:
                return HttpResponse(status=400, reason=e)
        try:
            items = get_store_items(account, sale_hashtag)
        except AssertionError as e:
            return JsonResponse({
                'error': str(e)
            })
        return redirect('items_list', account)


class ItemsList(View):
    http_method_names = ['get', ]

    def get(self, request, store):
        qs = Item.objects.filter(account__name=store).order_by('id')
        context = {
            'items': qs
        }
        return render(request, 'items_list.html', context)


class EditItem(View):
    def get(self, request, item_id):
        item = Item.objects.get(id=item_id)
        context = {
            'item': item
        }
        return render(request, 'edit_item.html', context)

    def post(self, request, item_id):
        data = request.POST
        item = Item.objects.get(id=item_id)

        name = data.get('name', '')
        price = data.get('price', Decimal('0'))
        description = data.get('description', '')

        item.name = name
        item.price = price
        item.description = description
        item.save()
        return redirect('items_list', item.account.name)

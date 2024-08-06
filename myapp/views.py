import json

from django.shortcuts import render,redirect
from .forms import ArticleForm
from .models import ouvrages
import datetime
from bson import ObjectId
from django.http import HttpResponse
from bson import json_util


def article_list(request):
    ouvrage = list(ouvrages.find())
    for article in ouvrage:
        if 'created_at' in article:
            article['id_str'] = str(article['_id'])
            article['created_at'] = article['created_at'].strftime('%Y-%m-%d %H:%M:%S')
    return render(request, 'article_list.html', {'articles': ouvrage})


def article_create(request):
    if request.method == "POST":
        form = ArticleForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            record = {
                "title": title,
                "content": content,
                "created_at": datetime.datetime.now(datetime.timezone.utc)
            }
            ouvrages.insert_one(record)
            form.save()
            return redirect('article_list')
    else:
        form = ArticleForm()
    return render(request, 'article_form.html', {'form': form})


def article_update(request, article_id):
    article = ouvrages.find_one({'_id': ObjectId(article_id)})
    if request.method == "POST":
        form = ArticleForm(request.POST)
        if form.is_valid():
            update_data = {}
            if form.cleaned_data['title']:
                update_data['title'] = form.cleaned_data['title']
            if form.cleaned_data['content']:
                update_data['content'] = form.cleaned_data['content']
            if update_data:
                ouvrages.update_one({'_id': ObjectId(article_id)}, {'$set': update_data})
            return redirect('article_list')
    else:
        form = ArticleForm(initial={
            'title': article.get('title', ''),
            'content': article.get('content', ''),
        })

    return render(request, 'article_form.html', {'form': form})


def export_database(request):
    documents = list(ouvrages.find())
    json_data = json.dumps(documents, default=json_util.default)
    response = HttpResponse(json_data, content_type='application/json')
    response['Content-Disposition'] = 'attachment; filename=exported_data.json'
    return response


def article_delete(request, article_id):
    if request.method == "GET":
        article = ouvrages.find_one({'_id': ObjectId(article_id)})
        print(article)
        return render(request, 'article_confirm_delete.html', {'article': article})
    else:
        ouvrages.delete_one({'_id': ObjectId(article_id)})
        return redirect('article_list')

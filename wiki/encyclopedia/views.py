from django.shortcuts import render
from django.http import HttpResponse
from markdown2 import Markdown
from . import util
import random

def convert_md_to_html(title):
    content = util.get_entry(title)
    markdowner = Markdown()
    if content == None:
        return None
    else:
        return markdowner.convert(content)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request,name):
    html_content = convert_md_to_html(name)
    if html_content == None :
        return render(request,"encyclopedia/error.html",{
            "message":"Sorry this entry does not exist"
        })
    else:
          return render(request,"encyclopedia/entry.html",{
            "title":name,
            "content":html_content
          })


def search(request):
    if request.method == "POST":
        entry_search = request.POST['q']
        html_content = convert_md_to_html(entry_search)
        if html_content is not None:
            return render(request,"encyclopedia/entry.html" , {
                "title" : entry_search ,
                 "content" : html_content})
        else:
            AllEntries = util.list_entries()
            recommandation = []
            for entry in AllEntries :
                if entry_search.lower() in entry.lower():
                    recommandation.append(entry)
            return render (request , 'encyclopedia/search.html' , {
                "recommandation":recommandation})  


def new_page(request):
    if request.method == "GET":
        return render(request,"encyclopedia/new.html")
    else:
        title = request.POST['title']
        content = request.POST['content']
        title_exist = util.get_entry(title)
        if title_exist is not None:
            return render (request,"encyclopedia/error.html",{
                "message":"Entry page altready exist"
            })
  
          
        else:
            util.save_entry(title,content)
            html_content = convert_md_to_html(title)
            return render(request,"encyclopedia/entry.html",{
                "title":title,
                "content":html_content

            })



def edit(request):
    if request.method == "POST":
        title = request.POST['entry_title']
        content = util.get_entry(title)
        return render(request,"encyclopedia/edit.html",{
            "title":title,
            "content":content

            })
    else:
        util.save_entry(name,content)
        html_content = convert_md_to_html(name)
        return render(request,"encyclopedia/entry.html",{
            "name" : name ,
            "content": html_content
        })


def save_edit(request):
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']
        util.save_entry(title,content)
        html_content = convert_md_to_html(title)
        return render(request,"encyclopedia/entry.html",{
            "title":title,
            "content":html_content
            })


def rand(request):
    Entries = util.list_entries()
    rand_entry = random.choice(Entries)
    html_content = convert_md_to_html(rand_entry)
    return render(request,"encyclopedia/entry.html",{
        "title":rand_entry,
        "content":html_content
    })
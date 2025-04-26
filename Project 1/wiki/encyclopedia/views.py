from django.shortcuts import render, redirect, HttpResponse
from django import forms
import markdown2
import random

from . import util

class CreateForm(forms.Form):
    title_name = forms.CharField(
        label="Title Name",
        widget=forms.Textarea(attrs={
            "class": "form-control",
            "placeholder": "Enter the title here",
            "rows": 2,
            "style": "resize: none;"
        })
    )
    title_content = forms.CharField(
        label="Title Content",
        widget=forms.Textarea(attrs={
            "class": "form-control",
            "placeholder": "Enter the content here",
            "rows": 6,
            "style": "resize: vertical;"
        })
    )

class EditForm(forms.Form):
    title_name = forms.CharField(
        label="Title",
        widget=forms.Textarea(attrs={
            "class": "form-control",
            "placeholder": "Enter title",
            "rows": 2,
            "style": "resize: none;"
        })
    )

    title_content = forms.CharField(
        label="Content",
        widget=forms.Textarea(attrs={
            "class": "form-control",
            "placeholder": "Enter content",
            "rows": 10,
            "style": "resize: vertical;"
        })
    )

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def title(request, title):
    content = util.get_entry(title)
    if not content:
        return render(request, "encyclopedia/error.html", {
            "message": "Page not found"
        })
    html_content = markdown2.markdown(content)
    return render(request, "encyclopedia/title.html", {
        "title":title,
        "content":html_content
    })

def search(request):
    searchquery = request.GET.get('q')
    if not searchquery:
        return redirect('encyclopedia:index')
    results = [] 
    if util.get_entry(searchquery):
        return redirect('encyclopedia:title', title=searchquery)
    else:
        all_entries=util.list_entries()
        for entry in all_entries:
            if searchquery.lower() in entry.lower():
                results.append(entry)
        if len(results) == 0:
            return render(request, "encyclopedia/error.html", {
                "message":"No possible pages not found"
            })
        return render(request, "encyclopedia/search.html", {
            "results":results,
            "search":searchquery
        })
    
def create(request):
    if request.method == "POST":
        form = CreateForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title_name"]
            content = form.cleaned_data["title_content"]

        all_entries = util.list_entries()
        for entry in all_entries:
            if entry.lower() == title.lower():
                return render(request, "encyclopedia/error.html", {
                    "message": "Page already Exists"
                })
            else:
                util.save_entry(title, content)
                return redirect('encyclopedia:index')
    
    return render(request, "encyclopedia/create.html", {
        "form": CreateForm()
    })

def edit(request, title):
    print(title)
    content = util.get_entry(title)
    if not content:
        return render(request, "encyclopedia/error.html", {
            "message": "Page not found"
        })
    
    if request.method == "POST":
        form = EditForm(request.POST)
        if form.is_valid():
            new_title = form.cleaned_data["title_name"]
            new_content = form.cleaned_data["title_content"]

            util.save_entry(new_title, new_content)
            return redirect("encyclopedia:title", title=new_title)
    else:
        form = EditForm(initial={
            "title_name": title,
            "title_content": content
        })

    return render(request, "encyclopedia/edit.html", {
        "form": form,
        "title": title
    })    

def randompage(request):
    all_entries=util.list_entries()
    if all_entries:
        random_number = random.randint(0, len(all_entries))
        entry = all_entries[random_number]
        return redirect("encyclopedia:title", title=entry)
    else:
        return redirect("encyclopedia:index")

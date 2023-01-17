from django.shortcuts import render
from django import forms
from . import util
from django.http import HttpResponseRedirect
from django.urls import reverse
import markdown2
import random

class NewPageForm(forms.Form):
    title = forms.CharField(label = "Title")
    content = forms.CharField(widget=forms.Textarea)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):   
    content = util.get_entry(title)
    if (content == None):
        return render(request, "encyclopedia/error.html", {
            "error": "This entry name doesn't exist"
        })
    else:
        content = markdown2.markdown(content)
        return render(request, "encyclopedia/entry.html", {
            "title" : title,
            "content": content
        })

def search(request):
    if request.method == "POST":
        title = request.POST['q']
        content = util.get_entry(title)
        if(content == None):
            list = util.list_entries()
            updated_list = []
            for el in list:
                if title.lower() in el.lower():
                    updated_list.append(el)
            return render(request, "encyclopedia/search.html", {
                "updated_list": updated_list
        })
        else:
            content = markdown2.markdown(content)
            return render(request, "encyclopedia/entry.html", {
                "title":title,
                "content": content
            })
    else:
        return render(request, "encyclopedia/layout.html")

def newpage(request):
    if (request.method == "POST"):
        form = NewPageForm(request.POST)
        data = request.POST
        if util.get_entry(data['title']) is not None:
            return render(request, "encyclopedia/error.html", {
                "error": "The title you entered already exists"
            })
        util.save_entry(data['title'], data['content'])
        content = markdown2.markdown(data['content'])
        return render(request, 'encyclopedia/entry.html', {
            "title" : data['title'],
            "content" : content
        })
    return render(request, "encyclopedia/newpage.html", {
        "form": NewPageForm()
    })

def editpage(request):
    if request.method == "POST":       
        title = request.POST['entry_title']
        content = util.get_entry(title)             
        return render(request, "encyclopedia/editpage.html", {
            "title": title,                         
            "content": content                      
        })                                      
    return render(request, "encyclopedia/editpage.html")            
                                        
def save_page(request):                             
    if request.method == "POST":                    
        title = request.POST['title']               
        content = request.POST['content']           
        util.save_entry(title , content)            
        content =  util.get_entry(title)                        
        content = markdown2.markdown(content)               
        return render(request, "encyclopedia/entry.html", {
            "title" : title,                         
            "content": content
        })

def random_page(request):
    all_title = util.list_entries()
    length = len(all_title)
    random_number = random.randint(0, length - 1)
    title = all_title[random_number]    
    content = util.get_entry(title)      
    content = markdown2.markdown(content)

    return render(request, "encyclopedia/entry.html", {
        "title" : title,                
        "content" : content             
    })                                  

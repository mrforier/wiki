from django import forms
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
import markdown2

from . import util




def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

class NewWikiForm(forms.Form):
    wikiname = forms.CharField(label="wikiname ")
    wiki = forms.CharField(widget=forms.Textarea, label="wiki entry ")
    # wikiname = forms.CharField(label="wikiname ", initial="one word no spaces")
    # wiki = forms.CharField(widget=forms.Textarea, label="wiki entry ", initial="use MD file formating")

def entry(request, entry):
    # print("entry: " + entry)

    # print(request)
    # print(util.get_entry(entry))
    if util.get_entry(entry):
        return render(request, "encyclopedia/wiki.html", {
            "wikibody": markdown2.markdown(util.get_entry(entry)),
            "title": entry
        })
    else:
        return render(request, "encyclopedia/wikierror.html", {
            "entry":entry
        })


def add(request):
    print("in add function")
    print(request)
    if request.method ==  "POST":
        print("add POST function")
        form = NewWikiForm(request.POST)
        print(form)
        print("form create")
        if form.is_valid():
            print("is valid")
            print(form.cleaned_data)
            title = form.cleaned_data["wikiname"]
            wikibody = form.cleaned_data["wiki"]
            print("wiki created")
            print(wikibody)
            #write the file
            
            if util.add_entry(title, wikibody):  
                print("added file")          
                return HttpResponseRedirect(reverse("wiki:index"))
                
            else:
                print("added file exctpion")
                return render(request, "encyclopedia/wikierror.html", {
                    "entry":"Could Not Create the File"
        })
    else:
        print("ready to render add")
        return render(request, "encyclopedia/addwiki.html", {
            "form": NewWikiForm()
        })

def edit(request):
    print("in edit function")
    #print("edit entry: " + entry)
    print(request)
    if request.method ==  "POST":
        print("edit POST function")
        form = NewWikiForm(request.POST)
        print(form)
        print("form edit")
        if form.is_valid():
            print("is valid")
            print(form.cleaned_data)
            title = form.cleaned_data["wikiname"]
            wikibody = form.cleaned_data["wiki"]
            print("wiki updated")
            print(wikibody)
            #write the file
            if util.edit_entry(title, wikibody):  
                print("updated file")          
                return HttpResponseRedirect(reverse("wiki:entry", args = (title,)))
     
            else:
                print("updated file exception")
                return render(request, "encyclopedia/wikierror.html", {
                    "entry":"Could Not Update the File"
        })
    else:
        print("in GET path for Edit Function")
        wikiname = request.GET.get('q', '')
        wiki = util.get_entry(wikiname)
        print(wikiname)
        print(wiki)
        if wiki:
            print("utl.get_entry section")
            print(entry)
            print(request)
            formdata = {
                "wikiname": wikiname,
                "wiki": wiki}
            print(formdata)
            return render(request, "encyclopedia/editwiki.html", {
                "form": NewWikiForm(formdata)
            })
        else:
            print(entry)
            return render(request, "encyclopedia/wikierror.html", {
                "entry":entry
            })

def error(request, entry):
    print("error entry: " + entry)
    print(request)
    return render(request, "encyclopedia/wikierror.html", {
        "entry": entry
    })




def search(request):
    print(request)
    query = request.GET.get('q', '')
    print("query  "+query)
    matchtype = "notset"
    search_run = util.search_match(query)
    matchtype = search_run[1]
    print("query "+ query)
    print("matchtype" + matchtype)
    print(search_run[1], search_run[0])
    if matchtype == "match":
        return render(request, "encyclopedia/wiki.html", {
            "wikibody": util.get_entry(query),
            "title": query
        })
    elif matchtype == "partial":
        return render(request, "encyclopedia/wikisearch.html", {
            "searchlist": search_run[0],
            "title": query
        })
    else:
        print("search else branch")
        print(type(request),query)
        return render(request, "encyclopedia/wikierror.html", {
            "entry": query
        })

def random_entry(request):
    print("random starts here")
    entry = util.random_entry()
    print("random called")
    print(entry)
    return HttpResponseRedirect(reverse("wiki:entry", args = (entry,)))




from django.shortcuts import render
from django.shortcuts import redirect
from encyclopedia.util import list_entries
from random import randrange

from . import util

import markdown2


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, entry_name):
    if util.get_entry(entry_name) == None:
        return render(request, "encyclopedia/no_entry_error.html")
    else:
        return render(request, "encyclopedia/entry.html", {
            "entry": markdown2.markdown(util.get_entry(entry_name)),
            "entry_name": entry_name
        })


def search(request):
    entry_name = request.POST.get("q")
    if entry_name in list_entries():
        return redirect("entry", entry_name)
    else:
        partial_match_list = []
        entry_name_low = entry_name.lower()
        for entry in list_entries():
            if entry_name_low in entry.lower():
                partial_match_list.append(entry)
        return render(request, "encyclopedia/search_results.html", {
            "matches": partial_match_list
        })


def new_entry(request):
    if request.method == "POST":
        entry_name = request.POST.get("entry_name")
        entry_content = request.POST.get("entry_content")
        if entry_name in util.list_entries():
            return render(request, "encyclopedia/entry_exists_error.html")
        else:
            f = open("entries/" + entry_name + ".md", "w")
            f.write("#" + entry_name + "\n\n" + entry_content)
            f.close()
            return redirect("entry", entry_name)
    else:
        return render(request, "encyclopedia/new_entry.html")


def edit(request, entry_name):
    if request.method == "POST":
        entry_content = request.POST.get("entry_content")
        f = open("entries/" + entry_name + ".md", "w")
        f.write(entry_content)
        f.close()
        return redirect("entry", entry_name)

    else:
        entry = util.get_entry(entry_name)
        return render(request, "encyclopedia/edit_entry.html", {
            "entry_name": entry_name,
            "entry": entry
        })


def random(request):
    entry_count = len(util.list_entries())
    random_num = randrange(0, entry_count)
    entry_name = util.list_entries()[random_num]
    return redirect("entry", entry_name)

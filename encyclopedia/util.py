import re

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage


def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    filenames = default_storage.listdir("entries")
    #print(filenames)
    filenames = filenames[1]
    #print(filenames)
    return list(sorted(re.sub(r"\.md$", "", filename)
        for filename in filenames if filename.endswith(".md")))


def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))


def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    matchtype = ""
    try:
        f = default_storage.open(f"entries/{title}.md")
        return f.read().decode("utf-8")
    except FileNotFoundError:
        return None


def search_match(query):
    """
    Compare search query to list of entiries, 
    Return match (call wiki page for match) or
    Return list of partial matches to search results page.
    """
    print("query: "+ query, query.lower(), type(query))
    searchlist = []
    matchtype = "nomatch"
    for entry in list_entries():
        print("entry" + entry, entry.lower())
        if query.lower() == entry.lower():
            searchlist.append(query)
            matchtype = "match"
            print("match")
            print(searchlist, matchtype)
            return searchlist, matchtype
        else:
            if query.lower() in entry.lower():
                searchlist.append(entry)
                matchtype = "partial"
    print("partial")
    print(searchlist, matchtype)
    return searchlist, matchtype

def add_entry(title, wiki):
    print("starting add_entry")
    print(title, wiki)
    try:
        print("in add try")
        f = default_storage.open(f"entries/{title}.md","x")
        f.write(wiki)
        print("worte file")
        f.close()
        return
    except:
        print("add try exception")
        return None





    
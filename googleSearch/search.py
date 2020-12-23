from googlesearch import search

query = "site:open.spotify.com/track " + input("Enter yo shit")
searches = search(term = query, num_results=5, lang = "en")

id5 = [search.replace("https://open.spotify.com/track/", "") for search in searches]
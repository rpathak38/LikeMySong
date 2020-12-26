import filter

genre_dictionary = filter.genres_dict("genres_classified.csv")

songs = []
# pass in possible songs here

target = None
# pass in target song here

output = filter.genre_filter(songs, target, genre_dictionary)
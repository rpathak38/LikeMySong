from googlesearch import search


class SongNotFound(Exception):
    """Exception raised for errors in the input song.
    Attributes:
        query -- query that caused error
        message -- explanation of the error
    """

    def __init__(self, query,
                 message="Whoops! The AI was unable to find that song! Please check your input and try again."):
        self.query = query
        self.message = message
        super().__init__(self.message)


def google_search(query):
    google_query = "site:open.spotify.com/track " + query
    searches = search(term=google_query, num_results=5, lang="en")

    id5 = [thing.replace("https://open.spotify.com/track/", "") for thing in searches]
    if len(id5) == 0:
        raise SongNotFound(query=query)
    else:
        return id5
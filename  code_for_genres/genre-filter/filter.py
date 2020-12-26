# sql: genres with their classification numbers
# our own methods, to call and receive possible genres based on a certain song id
from typing import List

from song_object import Song
from joblib import Parallel, delayed
import multiprocessing
import csv


def genres_dict(csv_file):
    with open(csv_file, "r") as fin:
        dictionary = {}
        csv_reader = csv.reader(csv_file)
        for genre, cluster in csv_reader:
            dictionary[genre] = cluster
        return dictionary


def genre_filter(songs: List[Song], target: Song, genre_dict: dict) -> List[Song]:
    """
    :param genre_dict: Dictionary of Genres grouped by cluster numbers
    :param songs: List of Song objects
    :param target: Target Song that all comparisons are done with respect to
    :return songs_out: Ordered List of Songs for display
    """

    songs_out = []

    def _ranker(possible_song):
        possible_song.genres = [genre_dict.get(genre) for genre in possible_song.genres if
                                genre_dict.get(genre) is not None]
        possible_song.similarity = 0
        possible_song.similarity = sum(el in target.genres for el in possible_song.genres)

        if possible_song.similarity > 0:
            songs_out.append(possible_song)

    results = Parallel(n_jobs=multiprocessing.cpu_count())(delayed(_ranker)(i) for i in songs)

    if songs_out == 0:
        return songs
    else:
        ranked_songs = results.sort(key=lambda song: song.similarity, reverse=True)
        return ranked_songs

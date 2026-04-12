from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import csv

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["id"] = int(row["id"])
            row["energy"] = float(row["energy"])
            row["tempo_bpm"] = float(row["tempo_bpm"])
            row["valence"] = float(row["valence"])
            row["danceability"] = float(row["danceability"])
            row["acousticness"] = float(row["acousticness"])
            songs.append(row)
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.
    Required by recommend_songs() and src/main.py

    Returns a tuple of (score, reasons) where score is out of 7.5 and
    reasons is a list of strings explaining each point contribution.
    """
    score = 0.0
    reasons = []

    # Genre match: +2.0 (hard categorical match)
    if song["genre"] == user_prefs.get("genre"):
        score += 2.0
        reasons.append(f"genre match ({song['genre']}) +2.0")

    # Mood match: +1.5 (soft categorical match)
    if song["mood"] == user_prefs.get("mood"):
        score += 1.5
        reasons.append(f"mood match ({song['mood']}) +1.5")

    # Energy proximity: up to +1.5
    energy_points = round((1 - abs(song["energy"] - user_prefs.get("energy", 0.5))) * 1.5, 2)
    score += energy_points
    reasons.append(f"energy proximity +{energy_points}")

    # Valence proximity: up to +1.0
    valence_points = round((1 - abs(song["valence"] - user_prefs.get("valence", 0.5))) * 1.0, 2)
    score += valence_points
    reasons.append(f"valence proximity +{valence_points}")

    # Danceability proximity: up to +0.8
    dance_points = round((1 - abs(song["danceability"] - user_prefs.get("danceability", 0.5))) * 0.8, 2)
    score += dance_points
    reasons.append(f"danceability proximity +{dance_points}")

    # Acousticness proximity: up to +0.7
    acoustic_points = round((1 - abs(song["acousticness"] - user_prefs.get("acousticness", 0.5))) * 0.7, 2)
    score += acoustic_points
    reasons.append(f"acousticness proximity +{acoustic_points}")

    return (round(score, 2), reasons)

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py

    Scores every song in the catalog, sorts by score descending, returns top k.
    Return format: list of (song_dict, score, explanation_string)
    """
    scored = [
        (song, *score_song(user_prefs, song))
        for song in songs
    ]
    ranked = sorted(scored, key=lambda x: x[1], reverse=True)
    return [(song, score, ", ".join(reasons)) for song, score, reasons in ranked[:k]]

import lyricsgenius as genius

class Scraper:
    def __init__(self):
        with open('key.txt') as file:
            self.key = file.readline()
        self.api = genius.Genius(self.key)
        self.api.skip_non_songs = True
    
    def get_lyrics(self, name, author):
        try:
            song = self.api.search_song(name, author)
            if len(song.lyrics) > 15000:
                return "Not Found"
            return song.lyrics
        except:
            return "Not Found"

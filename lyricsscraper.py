import lyricsgenius as genius

class Scraper:
    def __init__(self):
        with open('key.txt') as file:
            self.key = file.readline()
        self.api = genius.Genius(self.key)
        self.api.skip_non_songs = True
    
    def get_lyrics(self, name, author):
        song = self.api.search_song(name, author)
        if len(song.lyrics) > 15000:
            return "Not Found"
        return song.lyrics

'''
sc = Scraper()
l = sc.get_lyrics("Chain of Abuse (Visualizer)", "Three Days Grace")
print(l, len(l))
'''
import pickle

# Otwórz pliki wejściowe
with open('gameinfo.bin', 'rb') as file_gameinfo, \
     open('playerStats.csv', 'r') as file_playerStats, \
     open('HexRect.csv', 'r') as file_HexRect, \
     open('hexmap.csv', 'r') as file_hexmap:

    # Wczytaj dane z plików
    gameinfo_data = file_gameinfo.read()
    playerStats_data = file_playerStats.read()
    HexRect_data = file_HexRect.read()
    hexmap_data = file_hexmap.read()

    # Połącz dane w jeden słownik
    data = {
        'gameinfo': gameinfo_data,
        'playerStats': playerStats_data,
        'HexRect': HexRect_data,
        'hexmap': hexmap_data
    }

    # Zapisz dane w pliku binarnym
    with open('save_0.bin', 'wb') as file_combined:
        pickle.dump(data, file_combined)

data = None
from os import remove

# Usuń pliki
remove('gameinfo.bin')
remove('playerStats.csv')
remove('HexRect.csv')
remove('hexmap.csv')
my_id=0
# Otwórz plik binarny

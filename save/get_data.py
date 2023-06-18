import pickle
my_id = 3

with open(f'save_{my_id}.bin', 'rb') as file_combined:
    # Wczytaj dane
    data = pickle.load(file_combined)

# Odzyskaj dane z słownika
gameinfo_data = data['gameinfo']
playerStats_data = data['playerStats']
HexRect_data = data['HexRect']
hexmap_data = data['hexmap']

# Wykonaj odpowiednie operacje na danych...
with open('gameinfo.bin', 'wb') as file_gameinfo:
    file_gameinfo.write(gameinfo_data)

with open('playerStats.csv', 'w') as file_playerStats:
    file_playerStats.write(playerStats_data)

with open('HexRect.csv', 'w') as file_HexRect:
    file_HexRect.write(HexRect_data)

with open('hexmap.csv', 'w') as file_hexmap:
    file_hexmap.write(hexmap_data)

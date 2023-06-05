def split_text(text, chunk_size):
    chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
    return chunks

text = input("Wprowadź tekst: ")

chunk_size = int(input("Podaj ilość znaków na część: "))

result = split_text(text, chunk_size)

print("Podzielony tekst:")
for chunk in result:
    print(chunk)

from encrypt import encrypt, key_gen
import re
import copy

SPACE_CHAR = ' '

def new_letter_frequency(text):
    # Initialize a dictionary to store the frequency of each character
    # Initialize all the alphabets including space with count 0
    frequency = {}
    for char in ([chr(c) for c in range(97, 123)] + [SPACE_CHAR]):
        frequency[char] = 0

    # Count the frequency of each character in the text, including spaces
    for char in text:
        frequency[char] += 1

    # Sort the charcters by frequency in descending order
    sorted_frequency = dict(sorted(frequency.items(), key=lambda item: item[1], reverse=True))

    # Return sorted dictionary
    return sorted_frequency

def decrypt(ciphertext, plaintext): # Compare ciphertext frequencies to each plaintext file
    frequency_cipher = new_letter_frequency(ciphertext)
    frequency_plain = new_letter_frequency(plaintext)
   
    guessedtext = ''
    guessedtext_pointer = 0
    # Create the key by matching the ordered ciphertext frequency chars and the ordered plaintext frequency chars
    guessed_key = {}
    for char_plain, char_cipher in zip(list(frequency_plain.keys()), list(frequency_cipher.keys())):
        guessed_key[char_cipher] = char_plain

    # Using the key, guess the plaintext
    while (guessedtext_pointer < len(ciphertext)):
        guessedtext += guessed_key[ciphertext[guessedtext_pointer]]
        guessedtext_pointer += 1

    return guessedtext

def decrypt_dev(ciphertext): # Compare ciphertext frequencies to each plaintext file
    lowestDev = -1
    
    # Filter out all continuous characters (ex, 'aa', 'll')
    pre_char = '#'
    filtered_ciphertext = ''
    for char in ciphertext:
        if pre_char != char:
            filtered_ciphertext += char
            pre_char = char
        else:
            pre_char = char
            continue

    lowest_index = None

    SPACE_CHAR = ' '
    plaintext = ''
    for i in range(1,6):
        # Retrieve for each plaintext file
        plaintext_file = 'plaintexts/plaintext' + str(int(i)) + '.txt'
        plaintext = open(plaintext_file, 'r').readline().replace(' ', SPACE_CHAR)

        ciphertext = decrypt(filtered_ciphertext, plaintext)

        frequency_plain = new_letter_frequency(plaintext)
        frequency_cipher = new_letter_frequency(ciphertext)
        differenceSQ_sum = 0
        for j in range(len(frequency_cipher.values())):
            differenceSQ = abs(list(frequency_cipher.values())[j] - list(frequency_plain.values())[j]) ** 2
            differenceSQ_sum += differenceSQ
        standardDev = (differenceSQ_sum/len(frequency_cipher.values())) ** (0.5)
        print("Standard Deviation for plaintext",i,": ",standardDev)
        print(frequency_plain)
        if lowestDev == -1:
            lowestDev = standardDev
            lowest_index = i
        elif standardDev < lowestDev:
            lowest_index = i
            lowestDev = standardDev
    #print("The lowest Standard Deviation plaintext file is ", lowest_index)
    return lowest_index
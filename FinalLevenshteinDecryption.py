import re
# You should install Levenshtein package: pip install levenshtein
import Levenshtein 

SPACE_CHAR = ' '

def letter_frequency(text):
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

def decrypt_frequency(ciphertext, plaintext): 
    # Compare ciphertext frequencies to each plaintext file
    frequency_cipher = letter_frequency(ciphertext)
    frequency_plain = letter_frequency(plaintext)
   
    decryptedtext = ''
    decryptedtext_pointer = 0
    # Create the key by matching the ordered ciphertext frequency chars and the ordered plaintext frequency chars
    guessed_key = {}
    for char_plain, char_cipher in zip(list(frequency_plain.keys()), list(frequency_cipher.keys())):
        guessed_key[char_cipher] = char_plain

    # Using the key, guess the plaintext
    while (decryptedtext_pointer < len(ciphertext)):
        decryptedtext += guessed_key[ciphertext[decryptedtext_pointer]]
        decryptedtext_pointer += 1

    return decryptedtext

def decrypt_Levenshtein(ciphertext): # Compare ciphertext frequencies to each plaintext file
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

    lowest_score = -1
    lowest_index = None

    SPACE_CHAR = ' '
    plaintext = ''

    # Retrieve for each plaintext file
    for i in range(1,6):
        plaintext_file = 'plaintexts/plaintext' + str(int(i)) + '.txt'
        plaintext = open(plaintext_file, 'r').readline().replace(' ', SPACE_CHAR)

        # Decrypt the ciphertext using a letter frequency method first
        ciphertext = decrypt_frequency(filtered_ciphertext, plaintext)

        # 
        frequency_plain = letter_frequency(plaintext)
        frequency_cipher = letter_frequency(ciphertext)

        # Caculate Standard Deviation
        deviationSQ_sum = 0
        for j in range(len(frequency_cipher.values())):
            deviationSQ = abs(list(frequency_cipher.values())[j] - list(frequency_plain.values())[j]) ** 2
            deviationSQ_sum += deviationSQ
        variance = deviationSQ_sum/len(frequency_cipher.values())
        standardDev = (variance) ** (0.5)

        # Calculate Levenshtein Distance
        distance = Levenshtein.distance(ciphertext, plaintext)
        
        # Combine Standrad Deviation adn Levenshtein Distance
        # Here, the levenshtein distance is normalized (divided by 100) to avoid one overshadowing the other.
        dist_Dvi = standardDev + distance/100

        # Choose the plaintext index with the lowest sum value
        if lowest_score == -1 or dist_Dvi < lowest_score:
            lowest_score = dist_Dvi
            lowest_index = i

    return lowest_index

def main():
    ciphertext = input("Enter the ciphertext:")
    guessedtext_index = decrypt_Levenshtein(ciphertext)
    guessedtext_file = 'plaintexts/plaintext' + str(int(guessedtext_index)) + '.txt' 
    guessedtext = open(guessedtext_file, 'r').readline()
    print("My plaintext guess is:", guessedtext)
if __name__ == '__main__':
    main()


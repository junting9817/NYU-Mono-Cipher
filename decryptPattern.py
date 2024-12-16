from encrypt import encrypt, key_gen
import re
import copy

SPACE_CHAR = ' '

LETTERS = 'abcdefghijklmnopqrstuvwxyz'

def letter_frequency(text):
    # Initialize a dictionary to store the frequency of each character
    frequency = {}
    
    # Count the frequency of each character in the text, including spaces
    for char in text:
        if char in frequency:
            frequency[char] += 1
        else:
            frequency[char] = 1
    
    # Ensure space is included even if it doesn't appear in the text
    if ' ' not in frequency:
        frequency[' '] = 0
    
    # Sort the characters by frequency in descending order
    sorted_chars = sorted(frequency.items(), key=lambda item: item[1], reverse=True)
    
    # Create an array of frequencies in the same order as the sorted characters
    frequency_array = [count for _, count in sorted_chars]
    
    return frequency_array

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

def decrypt(ciphertext): # Compare ciphertext frequencies to each plaintext file
    frequency_cipher = new_letter_frequency(ciphertext)
    print("\nCIPHERTEXT")
    print(ciphertext)
    print("\nFREQUENCY ANALYSIS (CIPHERTEXT)")
    print(frequency_cipher)
   
   # Step 1 retrieve the frequencies of the other candidate plaintexts (there are a couple cached frequency sequences in the plaintext_stats folder)
   # Step 2 compare the frequencies of the ciphertext to the frequencies of the candidate plaintexts, and compute an error value
    SPACE_CHAR = ' '
    plaintext = ''
    lowest = 600
    global lowest_index
    lowest_index = 1
    for i in range(1,6):
        # Retrieve for each plaintext file
        plaintext_file = 'plaintexts/plaintext' + str(int(i)) + '.txt'
        plaintext = open(plaintext_file, 'r').readline().replace(' ', SPACE_CHAR)
        frequency_plain = new_letter_frequency(plaintext)
        #print(frequency_cipher)
        #print(frequency_plain)
        #print(sum(frequency_plain.values()))
        # Compare and find the lowest error between ciphertext frequencies and plaintext frequencies
        difference_sum = 0
        for j in range(len(frequency_cipher.values())):
            difference_sum += abs(list(frequency_cipher.values())[j] - list(frequency_plain.values())[j])
        print("Frequency error for plaintext",i,": ",difference_sum)
        print("Total: ",len(frequency_cipher.values()))
        if difference_sum < lowest:
             
            lowest_index = i
            lowest = difference_sum
            
    # Step 3 return the plaintext with the lowest error value   
    # Get a new sorted frequency for the lowest error plaintext     
    lowest_plaintext = open('plaintexts/plaintext' + str(int(lowest_index)) + '.txt', 'r').readline().replace(' ', SPACE_CHAR)
    lowest_frequency_plain = new_letter_frequency(lowest_plaintext)    
    print("The plaintext",lowest_index," has the lowest error")
    print("\nFREQUENCY ANALYSIS (PLAINTEXT)")
    print(lowest_frequency_plain)
    guessedtext = ''
    guessedtext_pointer = 0
    # Create the key by matching the ordered ciphertext frequency chars and the ordered plaintext frequency chars
    guessed_key = {}
    for char_plain, char_cipher in zip(list(lowest_frequency_plain.keys()), list(frequency_cipher.keys())):
        guessed_key[char_cipher] = char_plain
    print("GUESSED KEY IS: ")
    print(guessed_key)
    # Using the key, guess the plaintext
    while (guessedtext_pointer < len(ciphertext)):
        guessedtext += guessed_key[ciphertext[guessedtext_pointer]]
        guessedtext_pointer += 1

    return guessedtext


#########################################################
# Working on word pattern analyzing
# From the first part (above) of the decrypting, let's assume that the 'space' character is decrypted correctly.
# because 'space' character and letter 'e' are the most common characters in English.
# Then, we can split every word in the pre-decrypted ciphertext by 'space' character and words in the plaintext file, too.
# Also, we can analyze the word's pattern by detecting different types of letters used in each word in order.
# Even though there are some random insertions in the ciphertext, there still would be some words without any random insertions.
# Then, we might find some words with exact same patterns meaning that they are the same words. 
# With these found two words(plaintext and ciphertext), we can determine exact key values for the letters used in the word. 
# After searching all wordpatterns, we can find a new key (probably not full key).
# Using the new key, we will get closer guessed plaintext. 

def get_empty_cipher_letter_mapping():
    # Creating empty dictionary for letter mapping
    return {'a': [], 'b': [], 'c': [], 'd': [], 'e': [], 'f': [], 'g': [], 'h': [], 
    'i': [], 'j': [], 'k': [], 'l': [], 'm': [], 'n': [], 'o': [], 'p': [],'q': [], 
    'r': [], 's': [], 't': [], 'u': [], 'v': [], 'w': [], 'x': [], 'y': [], 'z': []}

def add_letters_to_mapping(letter_mapping, cipher_word, candidate):
    # Add deciphering candidate letters into the letter mapping 
    for i in range(len(cipher_word)):
        if candidate[i] not in letter_mapping[cipher_word[i]]:
            letter_mapping[cipher_word[i]].append(candidate[i])
    
def remove_solved_letters_from_mapping(letter_mapping):
    # Remove solved letters meaning that a cipher letter corresponds to only one mapping letter
    loop_again = True
    while loop_again:
        loop_again = False

        solved_letters = []
        for cipher_letter in LETTERS:
            if len(letter_mapping[cipher_letter]) == 1:
                solved_letters.append(letter_mapping[cipher_letter][0])
                for s in solved_letters:
                    if len(letter_mapping[cipher_letter]) != 1 and s in letter_mapping[cipher_letter]:
                        letter_mapping[cipher_letter].remove(s)
                        if len(letter_mapping[cipher_letter]) == 1:
                            loop_again = True
    return letter_mapping

def intersect_mapping(map_a, map_b):
    # Finding an intersection between two maps
    intersected_mapping = get_empty_cipher_letter_mapping()
    for letter in LETTERS:
        if map_a[letter] == []:
            intersected_mapping[letter] = copy.deepcopy(map_b[letter])
        elif map_b[letter] == []:
            intersected_mapping[letter] = copy.deepcopy(map_a[letter])
        else:
            for mapped_letter in map_a[letter]:
                if mapped_letter in map_b[letter]:
                    intersected_mapping[letter].append(mapped_letter)
    return intersected_mapping

def find_letter_mapping(message):

    # From the plaintext file with the lowest error, create patterns for all words in the plaintext
    allPatterns = all_patterns(lowest_index)
    
    intersected_map = get_empty_cipher_letter_mapping()
    cipher_word_list = message.split(' ')
    # For each word in ciphertext, analyze its word pattern and compare to the all patterns 
    # to check if the same pattern exist in the plaintext 
    for cipher_word in cipher_word_list:
        candidate_map = get_empty_cipher_letter_mapping()
        word_pattern = get_word_pattern(cipher_word)
        # If the pattern doesn't exist in all patterns in the plaintext, loop it again
        if word_pattern not in allPatterns:
            continue
        # If the pattern exists, add the candidate letters into the letter mapping
        for candidate in allPatterns[word_pattern]:
            add_letters_to_mapping(candidate_map, cipher_word, candidate)
        # Get the intersection between the already intersected map and new candidate map
        intersected_map = intersect_mapping(intersected_map, candidate_map)
    return remove_solved_letters_from_mapping(intersected_map)

def decrypt_with_letter_mapping(ciphertext, letter_mapping):
    # Create an empty key (here, no lowercases and space)
    key = ['_'] * len(LETTERS)
    for cipher_letter in LETTERS:
        # if a cipher letter eppears only once in the letter mapping, add to key. 
        if len(letter_mapping[cipher_letter]) == 1:
            key_index = LETTERS.find(letter_mapping[cipher_letter][0])
            key[key_index] = cipher_letter

    # Generate the key dictionary using the key values obtained above
    final_key = {' ':' '}
    for letter,keys in zip(list(LETTERS), key):
        if keys == '_':
            final_key[letter] = letter
        else:
            final_key[letter] = keys

    last_key = {' ':' '}

    for letter, keys in zip(list(LETTERS), key):
        if keys != '_':
            last_key[keys] = letter
    
    print("Second Key is")
    print(last_key)

    finaltext = ''
    finaltext_pointer = 0
    # with the key dictionary, guess the plaintext
    while (finaltext_pointer < len(ciphertext)):
        if ciphertext[finaltext_pointer] in last_key:
            finaltext += last_key[ciphertext[finaltext_pointer]]
        else:
            finaltext += ciphertext[finaltext_pointer]
        finaltext_pointer += 1

    return finaltext

def get_word_pattern(word):
    # Find the word pattern
    # (EX) 'A P P L I C A T I O N' -> '0.1.1.2.3.4.0.5.3.6.7'
    word = word.lower()
    next_num = 0
    letter_nums = {}
    word_pattern = []

    for letter in word:
        if letter not in letter_nums:
            letter_nums[letter] = str(next_num)
            next_num += 1
        word_pattern.append(letter_nums[letter])
    
    return '.'.join(word_pattern)

def all_patterns(lowest_index):
    # Find every pattern of all words in the selected plaintext file
    all_patterns = {}

    plaintext_file = 'plaintexts/plaintext' + str(int(lowest_index)) + '.txt'
    plaintext = open(plaintext_file, 'r').readline().replace(' ', SPACE_CHAR)
    word_list = plaintext.split(' ')

    for word in word_list:
        pattern = get_word_pattern(word)

        if pattern not in all_patterns:
            all_patterns[pattern] = [word]
        else:
            all_patterns[pattern].append(word)
    
    return all_patterns
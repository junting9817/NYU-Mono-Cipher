from encrypt import encrypt, key_gen
import re
import copy

SPACE_CHAR = ' '

LETTERS = 'abcdefghijklmnopqrstuvwxyz'
#non_letters_or_space_pattern = re.compile('[^a-z\s]')


#t = length of key
#key = number{0-26}^t
#cyphertext = {<space>, a,...,z}^t
# u = # of candidate plaintexts
# L = length of plaintext
# paramaters (L=600, u = 5, t = {1-20})
#each computed uses different variant of encryption scheme
#output = GUESS for L-Symbol plaintext

#Encryption -- Sequential (Two Options)
    #Option 1: Insert random value from {<space>,a, .... z}
        #-- Presumably, this still means the original encryption will be sustained i.e if the 
        # encrypted text is C then a random insertion would merely be C[0] + *random_value* + C[1:] rather than the other option C[0] + *random_value* +C[2:] (In this case the 0th index is being REPLACED instead of INSERTED)
    #Option 2: Add a cyphertext according to one of the schemes (YOU MAY CHOOSE THE SCHEMA)
        #Mono-Alphabetic (t = 27) ~ INCLUDES SPACES
            #-- [a,b,c... z] + [i,j,k...l]
            #-- Each letter gets bumped up by a constant amount, regardless of location or repitition
            #-- Key space: 27!
            #-- Ways to Solve: Frequency Analysis
        #Poly-Alphabetic (t << 27) ~ GUARENTEES REUSE?
            #-- Shift each element base on it's index%t
            #-- c = p + key[i%t]
            #-- keyspace: 27^t (but t << 27?)

#Testing requirements
    # Number of tests run (10)
    # Parameters L=600, u=5
    #Largest prob_of_random_cypher that program succeeeds on 
    #FILE_NAME: <last_name1>_<last_name2>_<last_name3>-decrypt
    #MUST RETURN OUTPUT WITHIN CERTAIN TIME
        # --first test = 1 minute upper (rough guess)
        # --second test = 3 minute upper (rough guess)
    #Only one cryptoanalysis per team

#Extra Credit
    # (1) Increase number of plaintext candidates and see if strategy works well, and also
    # try increasing the number of candidate plaintexts to see if it goes well (may relax
    # restriction) on x minutes of running time
    # When noting large increase for each prob_of_random_cyphertext value {0,0.05,0.1,0.15...0.75}; report pictures showing runtime and a function of nummber of candidate plaintexts

    #(2) ~Doing the same thing, but this time by increase prob_of_random_cyphertext, and
    # reporting its results as a function of time
 
#Question?
    #"new ciphertext, computed using the above encryption scheme (relatively to your chosen classical cipher; i.e. shift, monoalphabetic substitution or polyalphabetic substitution)"
        #So are we allowed to use shift or monoalphabetic?
        #Yes, if we choose mono, we will get tested with mono. If we choose poly, we will get tested with poly.
    #"plaintext dictionary with u=5 plaintexts"
        #Are we allowed to reference the plaintext dictionary in our code for use?
        #Yes, we can open it and use it inside the code.
    #"return the output plaintext on stdout within x minutes (or else it will be declared to default to an incorrect guess); most likely, we will choose x = 1 on test 1 and x = 3 on test 2."
        #What will be the parameters for the first test and second test? (i.e L=? t=? prob_of_random_ciphertext=?)
        #The first test is gauranteed to be a normal substitution cipher without randomness. From there, it seems like the prob_random_ciphertext increases by 5% every test.


# Most common first letter in a word in order of frequency
first_letter = ["","T", "O", "A", "W", "B", "C", "D", "S", "F", "M", "R", "H", "I", "Y", "E", "G", "L", "N", "O", "U", "J", "K"]

# Most common second letter in a word in order of frequency
second_letter = ["H", "O", "E", "I", "A", "U", "N", "R", "T"]

# Most common third letter in a word in order of frequency
third_letter = ["E", "S", "A", "R", "N", "I"]

# Most common last letter in a word in order of frequency
last_letter = ["E", "S", "T", "D", "N", "R", "Y", "F", "L", "O", "G", "H", "A", "K", "M", "P", "U", "W"]

# More than half of all words end with
common_word_endings = ["E", "T", "D", "S"]

# Letters most likely to follow 'E' in order of frequency
follow_e = ["R", "S", "N", "D"]

# Most common digraphs in order of frequency
digraphs = ["TH", "HE", "AN", "IN", "ER", "ON", "RE", "ED", "ND", "HA", "AT", "EN", "ES", "OF", "NT", "IS", "OU", "AR", "AS", "DE", "RT", "VE"]

# Most common trigraphs in order of frequency
trigraphs = ["THE", "AND", "THA", "ENT", "ION", "TIO", "FOR", "NDE", "HAS", "NCE", "TIS", "OFT", "MEN"]

# Most common double letters in order of frequency
double_letters = ["SS", "EE", "TT", "FF", "LL", "MM", "OO"]

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
    # print("\nCIPHERTEXT")
    # print(ciphertext)
    # print("\nFREQUENCY ANALYSIS (CIPHERTEXT)")
    # print(frequency_cipher)
   
   # Step 1 retrieve the frequencies of the other candidate plaintexts (there are a couple cached frequency sequences in the plaintext_stats folder)
   # Step 2 compare the frequencies of the ciphertext to the frequencies of the candidate plaintexts, and compute an error value
    SPACE_CHAR = ' '
    plaintext = ''
    lowest = 1200
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
        #print("Frequency error for plaintext",i,": ",difference_sum)
        if difference_sum < lowest:
            global lowest_index 
            lowest_index = i
            lowest = difference_sum
            
    # Step 3 return the plaintext with the lowest error value   
    # Get a new sorted frequency for the lowest error plaintext     
    #lowest_plaintext = open('plaintexts/plaintext' + str(int(lowest_index)) + '.txt', 'r').readline().replace(' ', SPACE_CHAR)
    #lowest_frequency_plain = new_letter_frequency(lowest_plaintext)    
    # print("The plaintext",lowest_index," has the lowest error")
    # print("\nFREQUENCY ANALYSIS (PLAINTEXT)")
    # print(lowest_frequency_plain)
    '''guessedtext = ''
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
        guessedtext_pointer += 1'''

    return lowest_index
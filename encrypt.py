import random

# Determine where space should be ' ' or '_'.
SPACE_CHAR = ' '

# Random probability percent.
#PROB_RND = 0.05

def key_gen():
    chars = [chr(c) for c in range(97, 123)] + [SPACE_CHAR]
    chars_shuffled = chars[:]
    random.shuffle(chars_shuffled)

    '''
        For each c in chars, map the corresponding cs in chars_shuffled. That is:
        c[0] -> cs[0]
        c[1] -> cs[1]
        c[2] -> cs[2]
        ...
    '''
    key = {}
    for i in range(len(chars)):
        key[chars[i]] = chars_shuffled[i]

    #print(key)

    return key

def encrypt(plaintext,prob_rnd, key):
    ciphertext = ''
    plaintext_pointer = 0
    num_rnd = 0

    while (plaintext_pointer < len(plaintext) and plaintext[plaintext_pointer] != '\n'):
        coin = random.random()
        if prob_rnd <= coin <= 1:   # Encrypt based on key.
            ciphertext += key[plaintext[plaintext_pointer]]
            plaintext_pointer += 1
        elif 0 <= coin < prob_rnd:  # Insert random char.
            ciphertext += random.choice([chr(c) for c in range(97, 123)] + [SPACE_CHAR])
            num_rnd += 1
            #print('inserted random ciphertext', ciphertext[-1], ' at index ', plaintext_pointer)

    return ciphertext


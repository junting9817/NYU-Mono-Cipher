from encrypt import encrypt, key_gen
from decryptLevenshtein import decrypt_Levenshtein
import random

SPACE_CHAR = ' '
correct = 0
wrong = 0

for i in range(1000): 
    answer = random.randint(1,5)
    plaintext_file = 'plaintexts/plaintext' + str(answer) + '.txt'
    plaintext = open(plaintext_file, 'r').readline().replace(' ', SPACE_CHAR)

    ciphertext = encrypt(plaintext.lower(), 0.50, key_gen())

    res = decrypt_Levenshtein(ciphertext)
    if(res == answer):
        correct += 1
    else:
        wrong += 1

print("Total # of correct guesses: ", correct)
print("Total # of wrong guesses: ", wrong) 
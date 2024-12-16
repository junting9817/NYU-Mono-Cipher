from encrypt import encrypt, key_gen
from decryptDeviation import decrypt_dev, new_letter_frequency
import random

SPACE_CHAR = ' '
correct = 0
wrong = 0

for i in range(1,1001): 
    answer = random.randint(1,5)
    plaintext_file = 'plaintexts/plaintext' + str(answer) + '.txt'
    plaintext = open(plaintext_file, 'r').readline().replace(' ', SPACE_CHAR)
    frequency = new_letter_frequency(plaintext)
    #print("\nFREQUENCY ANALYSIS (PlAINTEXT)")
    #print(frequency)

    ciphertext = encrypt(plaintext.lower(), 0.20, key_gen())

    res = decrypt_dev(ciphertext)
    if(res == answer):
        correct += 1
    else:
        wrong += 1

print("Total # of correct guesses: ", correct)
print("Total # of wrong guesses: ", wrong) 
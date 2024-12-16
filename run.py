from encrypt import encrypt, key_gen
from decrypt import decrypt, letter_frequency, new_letter_frequency
import random

SPACE_CHAR = ' '
    #create a frequency sequence for each plaintext using frequency
print("DO NOT USE ANY SYMBOLS IN THE CIPHERTEXT")
# plaintext = input("Enter the ciphertext:")
answer = random.randint(1,5)
plaintext_file = 'plaintexts/plaintext' + str(answer) + '.txt'
plaintext = open(plaintext_file, 'r').readline().replace(' ', SPACE_CHAR)
frequency = new_letter_frequency(plaintext)
print("\nFREQUENCY ANALYSIS (PlAINTEXT)")
print(frequency)

ciphertext = encrypt(plaintext.lower(), 0.20, key_gen())

    #frequency sequence for all the plaintexts and the ciphertext
print("---------------------------------------------------")
res = decrypt(ciphertext)
# print("\nRESULTS")
# print(res)
# print("\n\nORIGINAL TEXT")
if(res == answer):
    print("CORRECT")
else:
    print("WRONG")
# print(plaintext) 
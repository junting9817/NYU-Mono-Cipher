from encrypt import encrypt, key_gen
from decryptLevenshtein import decrypt_Levenshtein
import random

SPACE_CHAR = ' '
    #create a frequency sequence for each plaintext using frequency
print("DO NOT USE ANY SYMBOLS IN THE CIPHERTEXT")
answer = random.randint(1,5)
plaintext_file = 'plaintexts/plaintext' + str(answer) + '.txt'
plaintext = open(plaintext_file, 'r').readline().replace(' ', SPACE_CHAR)
ciphertext = encrypt(plaintext.lower(), 0.20, key_gen())

res = decrypt_Levenshtein(ciphertext)
if(res == answer):
    print("CORRECT")
    print("Cipher Text Result: ", res)
    print("Original Plain Text: ", answer)
else:
    print("WRONG")
    print("Cipher Text Result: ", res)
    print("Original Plain Text: ", answer)

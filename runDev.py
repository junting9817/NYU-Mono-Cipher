from encrypt import encrypt, key_gen
from decryptDeviation import decrypt, new_letter_frequency
import random

SPACE_CHAR = ' '
    #create a frequency sequence for each plaintext using frequency
print("DO NOT USE ANY SYMBOLS IN THE CIPHERTEXT\n")
# plaintext = input("Enter the ciphertext:")
answer = random.randint(1,5)
plaintext_file = 'plaintexts/plaintext' + str(answer) + '.txt'
plaintext = open(plaintext_file, 'r').readline().replace(' ', SPACE_CHAR)
frequency = new_letter_frequency(plaintext)
print(plaintext)
#print("\nFREQUENCY ANALYSIS (PlAINTEXT)")
#print(frequency)

ciphertext = encrypt(plaintext.lower(), 0.20, key_gen())

    # Ciphertext
print("---------------------------------------------------")
print(ciphertext)
'''print(len(ciphertext))
frequency_cipher = new_letter_frequency(ciphertext)
print(frequency_cipher)
print(sum(frequency_cipher.values()))
res = decrypt(ciphertext)
if(res == answer):
    print("CORRECT")
    print("Cipher Text Result: ", res)
    print("Original Plain Text: ", answer)
else:
    print("WRONG")
    print("Cipher Text Result: ", res)
    print("Original Plain Text: ", answer)'''
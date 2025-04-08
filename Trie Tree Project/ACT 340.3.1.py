def string_mod(first, *output: tuple):
    print(first); 
    for change, second in output:
        print(change); print(second);
    print()

one = "You learn more from failure than from success."
string_mod(one, ("Replacing all . with !", one.replace('.', '!')))

two = "WHEN YOU Change your thougHts, remember to ALSO change your world."
string_mod(two, ("Making all lowercase...", two.lower()), ("Making all uppercase...", two.upper()))

four = "There are no traffic jams along the extra mile."
string_mod(four, ("This string starts with Z", four.startswith('Z')), ("Does it start with t?", four.startswith('t')), ("Well at what index is the character j in this string?", four.index('j')))

t_count, o_count = four.count('t'), four.count('o')
print(f"The letter t is present {t_count} times, and the letter o is present {o_count} times. \n")

greeting = "Good Morning!"
string_mod(greeting, ("How long is this string?", f"{len(greeting)} characters."))

alphabet = "abcdefghijklmnopqrstuvwxyz"
string_mod(alphabet, ("This string only contains alpha characters.", alphabet.isalpha()))

learning = "Learning is fun!"
string_mod(learning, ("Where is the character y in this string?", learning.find('y')))
print("Well that's not really an index so I'd better not use the index method or it might throw an error. \n")
# print(learning.index('y'))
# The find method and index method have the same functionality
# However, find returns -1 when a character is not found while index throws an error

count_string = "Twinkle twinkle little star, how I wonder what your are"
char_set = set(count_string)
string_mod(count_string, ("To find the frequency of each character, we have to find each unique character first. Let's cast it to a set!", char_set))

print("Now let's find the frequency of each character. \n")
for char in char_set:
    print(f"{char} : {count_string.count(char)}")
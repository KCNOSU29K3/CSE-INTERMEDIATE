#! /usr/bin/env python3
import random


def main():

    # define lists for dictionary construction
    english_words = [
        "sir", "hotel", "student", "boy", "madam", "professor", "restaurant", "your", "excuse",
        "students", "are", "lawyer", "the", "restroom", "my", "hello", "is", "man"
        ]
    
    pirate_words = [
        "matey", "fleabag inn", "swabbie", "matey", "proud beauty", "foul blaggart", "galley", "yer", "arr",
        "swabbies", "be", "foul blaggart", "th'", "head", "me", "avast", "be", "matey"
    ]
    
    # intro + showing of translatable words
    print("This is a translator for pirate language.")
    print("Current supported words are:")
    sample = random.sample(english_words, 6)
    for i in sample: print(i)

    # get word to translate and construct dictionary.
    str_to_translate = input("Please enter a phrase to translate.\n").split(" ")
    translate_dict = {english:pirate for (english, pirate) in zip(english_words, pirate_words)}

    # process translation
    output_dir = []
    for i in str_to_translate:
        if translate_dict.get(i) is not None:
            output_dir.append(translate_dict[i])
        else:
            output_dir.append(i)
    
    # output
    print(output_dir)
    print(f"Translated string is: {' '.join(output_dir)}")

if __name__ == "__main__":
    main()
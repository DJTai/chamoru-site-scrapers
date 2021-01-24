import shelve

from chamoru_data import ChamoruWord


def get_chamoru_dict():
    """Retrieves the dictionary stored in the shelf object.

    Returns:
        dict: Dictionary stored in shelf object.
    """
    shelf_file = 'chamoru_dictionary.db'
    ch_shelve = shelve.open(shelf_file)
    ch_dict = ch_shelve['dictionary']

    return ch_dict


def main():
    """Main function"""

    chamoru_dict = get_chamoru_dict()
    done = False

    while not done:
        word_to_search = input("Search for (leave blank to exit): ")
        if word_to_search == '':
            print("Exiting. Saina Ma'åse'")
            done = True
        else:
            word_found = chamoru_dict.get(word_to_search)
            print(word_found)
            print()

if __name__ == "__main__":
    main()

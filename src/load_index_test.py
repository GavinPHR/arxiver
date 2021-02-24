import utils

if __name__=="__main__":
    index = utils.load_index()

    while True:
        print("Enter a word to search the index for:")
        x = input()

        try:
            print(index[x])
        except KeyError:
            print("Sorry, this word is not in the index. Try another.")
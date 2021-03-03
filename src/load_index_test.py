from src import utils
import time

if __name__=="__main__":
    start_time = time.time()
    index = utils.load_index(filename="indexes/inverted_index_t")
    end_time = time.time()
    print("Took {} seconds to load".format(end_time-start_time))

    while True:
        print("Enter a word to search the index for:")
        x = input()

        try:
            print(index[x])
        except KeyError:
            print("Sorry, this word is not in the index. Try another.")
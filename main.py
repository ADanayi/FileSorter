import os
import sorter

print("This main is running!")
unsorted = os.path.join(os.getcwd(), "Unsorted")
sorted = os.path.join(os.getcwd(), "Sorted")
n_sorted = sorted
i = 0
while os.path.exists(n_sorted):
    i += 1
    n_sorted = sorted + "_" + str(i)

my_sort = sorter.Sorter(unsorted, n_sorted)
my_sort.sort()

print("Ended")
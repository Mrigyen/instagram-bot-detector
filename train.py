import csv

# read in csv
with open('training/labelled_1000_inclprivate.csv', 'rt', encoding="utf8") as csvfile:
    dataset = csv.reader(csvfile, delimiter=",", quotechar="|")
    for row in dataset:
        print(', '.join(row))

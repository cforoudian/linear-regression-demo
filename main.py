import math
from regression import Regr


def main():

    path = "data.csv"

    regr = Regr(path)

    regr.calculateGeneralStats()
    
    generalStats = regr.calculateRegrLine()

    print("General Stats: " + str(generalStats))


if __name__ == "__main__":
    main()
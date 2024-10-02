import csv
import math

class Regr():

    # handled dataset
    dataset = []

    # contains -> x, y, (x - x^), (y - y^), (x-x^) * (y-y^), (x-x^ ^2), (y-y^ ^2)
    calculatedDataset = []

    # contains means, cov, vars, r, stdevs, m, b of dataset
    generalDatasetStats = []


    # initialized and reads csv into dataset
    def __init__(self, path) -> None:

        file_path = path

        with open(file_path, mode='r') as file:
            reader = csv.reader(file)

            headers = next(reader)
            print("Headers: " + str(headers))

            for i in reader:
                print(i)
                tup = (float(i[0]), int(i[1]))
                self.dataset.append(tup) # expandable later
            
            print()

    # called by main to begin calculations of general stats needed for regression
    def calculateGeneralStats(self):
        x_mean, y_mean = self.__getMean(self.dataset)
        self.calculatedDataset = self.__calcVarCov(self.dataset, x_mean, y_mean)
        xy_cov, x_var, y_var = self.__summations(self.calculatedDataset)
        r = self.__calcPearsons(xy_cov, x_var, y_var)

        x_std, y_std = self.__calcStds(x_var, y_var, self.dataset)

        self.generalDatasetStats.append(x_mean, y_mean, xy_cov, x_var, y_var, r, x_std, y_std)

    
    # once calculateGeneralStats is called, main calls this next to use general stats to perform linear regression
    def calculateRegrLine(self):
        m = self.__calcSlope(self.generalDatasetStats[5], self.generalDatasetStats[6], self.generalDatasetStats[7])
        self.generalDatasetStats.append(m)
        b = self.__calcIntercept(self.generalDatasetStats[7], self.generalDatasetStats[0], self.generalDatasetStats[1])
        self.generalDatasetStats.append(b)

        print("REGRESSED LINEAR FORMULA OF DATA:")
        print("\ty = " + str(m) + "x + " + str(b))

        return self.generalDatasetStats

    ### ------------------------------------------------------------------------------------------------------------
    
    # calculates the mean of both x and y in the dataset
    def __getMean(self, dataset):
        print("CALCULATING MEAN...")

        x_mean = sum(x[0] for x in dataset) / len(dataset)
        y_mean = sum(y[1] for y in dataset) / len(dataset)

        print("> X_MEAN: " + str(x_mean))
        print("> Y_MEAN: " + str(y_mean))
        print()

        return x_mean, y_mean
    
    # in charge of procedures to reach general stat values of the data
    def __calcVarCov(self, dataset, x_mean, y_mean):
        print("CALCULATING DATASET's VARS AND COVS SUMMATIONS...")
        calcDataset = []

        for count in dataset:
            x_error = count[0] - x_mean
            y_error = count[1] - y_mean
            xy_cov_step = x_error * y_error
            x_var_step = x_error**2
            y_var_step = y_error**2
            print(str(type(xy_cov_step)) + "--------------" + str(xy_cov_step))
            calcDataset.append((count[0], count[1], xy_cov_step, x_var_step, y_var_step))
            print(calcDataset)

        xy_cov, x_var, y_var = self.__summations(calcDataset)

        return xy_cov, x_var, y_var
    

    # called by __calcVarCov to do summations for general stats
    def __summations(self, data):

        for val in data:
            print(str(type(val)))

        xy_cov = round(sum(val[2] for val in data),1)
        x_var = round(sum(val[3] for val in data if len(val) == 5),1)
        y_var = round(sum(val[4] for val in data if len(val) == 5),1)

        print("COV: " + str(xy_cov))
        print("X_VAR: " + str(x_var))
        print("Y_VAR: " + str(y_var))
        print()

        return xy_cov, x_var, y_var
    

    # calculates Pearson's Coefficient to be able to solve slope equation
    def __calcPearsons(self, xy_cov, x_var, y_var):
        print("CALCULATING PEARSONS COEFFICIENT...")

        r = round(xy_cov / (math.sqrt(x_var * y_var)),3)

        print("R: " + str(r))
        print()

        return r
    

    # calculates standard deviations using x and y variances
    def __calcStds(self, x_var, y_var, dataset):
        print("CALCULATING STD'S OF X AND Y...")

        x_std = round(math.sqrt(x_var / (len(dataset) - 1)),3)
        y_std = round(math.sqrt(y_var / (len(dataset) - 1)),3)

        print("X_STD: " + str(x_std))
        print("Y_STD: " + str(y_std))
        print()

        return x_std, y_std
    

    # calculates slope using r and x/y standard deviations
    def __calcSlope(self, r, x_std, y_std):
        print("CALCULATING SLOPE...")

        m = round(r * (y_std / x_std),3)

        print("SLOPE: " + str(m))
        print()
    

    # calculates y-int using newly found slope
    def __calcIntercept(self, m, x_mean, y_mean):
        print("CALCULATING Y-INTERCEPT...")

        a = round(y_mean - (m * x_mean),3)

        print("Y-INT: " + str(a))
        print()
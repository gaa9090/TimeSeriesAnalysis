import pandas as pd
import numpy as np


class test_program():
    # load data
    def __init__(self):
        self.df = np.loadtxt("csv_files/MonthlyGlobalTemperature.csv", delimiter=",", skiprows=1, usecols=2)
        
    # see data 
    def test_upload_file(self):
        print(self.df)

    # generate fake data
    def test_generate_fake_series(self, seed):
        np.random.seed(42)
        date_range = pd.date_range(start="2024-01-01", periods=100, freq="D")

        data = {
            "Date": date_range,
            "Value": np.random.normal(loc=100, scale=10, size=100)  # Normally distributed values
        }

        self.df = pd.DataFrame(data)
        self.df.to_csv("fake_time_series.csv", index=False)

    def test_see_data_head():
        pass
    def test_see_data_all():
        pass



if __name__ == "__main__":
    test = test_program()
    test.test_upload_file()
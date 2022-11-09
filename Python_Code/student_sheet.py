import tomllib
import pandas as pd

#with open("student.toml", "rb") as f:
#    data = tomllib.load(f)

data = pd.read_csv("students.csv")
filter_data = data[['Student','ID']]
to_list = filter_data.values.tolist()

new_data = to_list[1::]
print(new_data)

    





import pandas as pd

src_file = "MLX90640 example data.xlsx"
data = pd.read_excel(src_file)
print(data.head())
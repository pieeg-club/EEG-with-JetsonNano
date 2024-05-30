import pandas as pd
import matplotlib.pyplot as plt

# Load the Excel file into a DataFrame
df = pd.read_excel("output1.xlsx")

# Assuming you want to visualize data from columns data_1ch_test to data_8ch_test
columns_to_visualize = ['data_1ch_test', 'data_2ch_test', 'data_3ch_test', 'data_4ch_test', 'data_5ch_test', 'data_6ch_test', 'data_7ch_test', 'data_8ch_test']

# Plotting each column separately
for column in columns_to_visualize:
    plt.plot(df[column], label=column)

plt.xlabel('Index')
plt.ylabel('Value')
plt.title('Data Visualization')
plt.legend()
plt.show()

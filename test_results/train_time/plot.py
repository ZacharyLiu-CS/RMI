import matplotlib.pyplot as plt
import pandas as pd
from pprint import pprint
data_size_df = pd.read_csv('data_size.csv', delimiter=',')
train_time_df = pd.read_csv('train_time.csv', delimiter=',')

# pprint(train_time_data)
# Merge the two dataframes on 'index_type' and 'data_set'
merged_df = pd.merge(data_size_df,train_time_df, on=['index_type', 'data_set'], how='outer')

# pprint(merged_df)
# Convert 'size' columns to numeric and convert 'ns' to a float for time in nanoseconds

for col in merged_df.columns:
    if '_y' in col:
        # pprint(merged_df[col])
        for i in range(merged_df[col].size):
            if isinstance(merged_df[col][i],str):
                merged_df.loc[i, col] = float(merged_df[col][i][:-2])
    if '_x' in col:
        for i in range(merged_df[col].size):
            if isinstance(merged_df[col][i],str):
                suffix = merged_df[col][i][-2:]
                data_part = float(merged_df[col][i][:-2])
                if suffix == "MB":
                    merged_df.loc[i, col] = 1024 * data_part
                elif suffix == "GB":
                    merged_df.loc[i, col] = 1024 * 1024* data_part
                else:
                    merged_df.loc[i, col] = data_part
pprint(merged_df)
# Drop rows where 'size' or 'ns' are NaN after conversion
# merged_df = merged_df.dropna(subset=['size0', 'size1', 'size2', 'size3', 'size4'])

# Setup the plot
plt.figure(figsize=(12, 8))

for index_type in merged_df['index_type'].unique():
    mask = merged_df['index_type'] == index_type
    sizes = merged_df.loc[mask, 'size0_x']  # You can modify this to average sizes or choose a specific size
    times = merged_df.loc[mask, 'size0_y']  # Same as sizes for this example, change as needed

    plt.plot(sizes, times, label=index_type)

plt.title('Index Size vs Training Time')
plt.xlabel('Index Size (Bytes)')
plt.ylabel('Training Time (ns)')
plt.legend(title='Index Type')
plt.grid(True)

# Show the plot
plt.show()
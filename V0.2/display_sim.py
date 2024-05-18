import csv
import csv

import matplotlib.pyplot as plt

# Open the CSV file
import matplotlib.pyplot as plt

# Open the CSV file
with open('V0.2/test/test.csv', 'r') as file:
    # Read the data from the CSV file
    reader = csv.reader(file)
    dataNames = next(reader)

    # Create a dictionary to store the data
    data = {}
    for row in reader:
        if len(row) == 0:
            continue
        time = float(row[0])
        for i in range(1, len(row)):
            value = float(row[i])
            if i not in data:
                data[i] = []
            data[i].append((time, value))

# Plot each value separately
for i, values in data.items():
    times = [t for t, _ in values]
    values = [v for _, v in values]
    fig, ax = plt.subplots()
    ax.plot(times, values, label=str(dataNames[i])+ ' vs Time')
    ax.set_xlabel('Time')
    ax.set_ylabel(str(dataNames[i]))
    ax.set_title(str(dataNames[i])+ ' vs Time')
    ax.legend()
    ax.grid(True)

# Display all the plots on the screen
plt.show()

import matplotlib.pyplot as plt
import datetime

# Example dataset (dates and velocities)
dates = [
    datetime.datetime(2023, 1, 1),
    datetime.datetime(2023, 1, 2),
    datetime.datetime(2023, 1, 3),
    datetime.datetime(2023, 1, 4),
    datetime.datetime(2023, 1, 5),
    datetime.datetime(2023, 1, 6),
    datetime.datetime(2023, 1, 7)
]

velocities = [10, 12, 8, 15, 11, 9, 13]

# Sprints (target velocities)
sprint_dates = [
    datetime.datetime(2023, 1, 1),
    datetime.datetime(2023, 1, 3),
    datetime.datetime(2023, 1, 5),
    datetime.datetime(2023, 1, 7)
]

sprint_targets = [10, 15, 12, 14]

# Convert dates to matplotlib format
mpl_dates = plt.date2num(dates)
mpl_sprint_dates = plt.date2num(sprint_dates)

# Create a figure and axis
fig, ax = plt.subplots()

# Plot the velocity chart
ax.plot(mpl_dates, velocities, label='Velocity')

# Add sprints as reference lines
for date, target in zip(mpl_sprint_dates, sprint_targets):
    ax.axhline(target, color='r', linestyle='--', label='Sprint Target')
    ax.text(mpl_dates[0], target, f" Sprint Target: {target}", color='r', ha='right', va='center')

# Format the x-axis as dates
date_format = matplotlib.dates.DateFormatter("%m-%d-%Y")
ax.xaxis.set_major_formatter(date_format)
fig.autofmt_xdate()

# Set axis labels and title
ax.set_xlabel("Date")
ax.set_ylabel("Velocity")
ax.set_title("Velocity Chart")

# Display the legend
ax.legend()

# Display the chart
plt.show()

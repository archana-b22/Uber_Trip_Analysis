import pandas as pd
import matplotlib.pyplot as plt
#Load dataset
df = pd.read_csv("dataset/Uber-Jan-Feb-FOIL.csv")
print(df.head())
print(df.info())
print(df.isnull().sum())
print("Duplicates:",df.duplicated().sum())
#converting date column to datetime
df['date'] = pd.to_datetime(df['date'])
print(df.info())
df["month"] = df['date'].dt.month
df['day'] = df['date'].dt.day
df['weekday'] = df['date'].dt.day_name()
print(df.head())
# total trips per month 
trips_per_month = df.groupby("month")["trips"].sum()
print(trips_per_month)
# Plot trips per month
plt.figure(figsize=(6,4))
plt.bar(trips_per_month.index, trips_per_month.values)
plt.xlabel("Month")
plt.ylabel("Total Trips")
plt.title("Total Uber Trips per Month")
plt.tight_layout()

# Save the graph into images folder
plt.savefig("images/trips_per_month.png")

plt.show()
# Total trips per weekday
trips_per_weekday = df.groupby("weekday")["trips"].sum()
print(trips_per_weekday)

# Plot trips per weekday
plt.figure(figsize=(7,4))
plt.bar(trips_per_weekday.index, trips_per_weekday.values)
plt.xlabel("Weekday")
plt.ylabel("Total Trips")
plt.title("Total Uber Trips per Weekday")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("images/trips_per_weekday.png")
plt.show()
# Total active vehicles per weekday
vehicles_per_weekday = df.groupby("weekday")["active_vehicles"].sum()
print(vehicles_per_weekday)

# Plot active vehicles per weekday
plt.figure(figsize=(7,4))
plt.bar(vehicles_per_weekday.index, vehicles_per_weekday.values, color='orange')
plt.xlabel("Weekday")
plt.ylabel("Active Vehicles")
plt.title("Active Vehicles per Weekday")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("images/active_vehicles_per_weekday.png")
plt.show()
# Find the day with highest trips
max_trip_day = df.loc[df["trips"].idxmax()]
print("Day with Highest Trips:")
print(max_trip_day)

# Find the day with lowest trips
min_trip_day = df.loc[df["trips"].idxmin()]
print("\nDay with Lowest Trips:")
print(min_trip_day)
#save cleaned dataset to excel folder
df.to_csv("excel/uber_cleaned_data.csv", index=False)
print("cleaned file saved successfully!")
import sqlite3

# Create or connect to database
conn = sqlite3.connect("sql/uber.db")
cursor = conn.cursor()

# Load cleaned dataframe into SQL table
df.to_sql("uber_data", conn, if_exists="replace", index=False)

print("SQL table created successfully!")
# 1. Total trips
cursor.execute("SELECT SUM(trips) FROM uber_data")
print("\nTotal Trips:", cursor.fetchone()[0])

# 2. Trips per weekday
cursor.execute("SELECT weekday, SUM(trips) FROM uber_data GROUP BY weekday")
print("\nTrips Per Weekday:")
for row in cursor.fetchall():
    print(row)

# 3. Busiest day (max trips)
cursor.execute("SELECT date, trips FROM uber_data ORDER BY trips DESC LIMIT 1")
print("\nBusiest Day:", cursor.fetchone())

# 4. Least busy day (min trips)
cursor.execute("SELECT date, trips FROM uber_data ORDER BY trips ASC LIMIT 1")
print("Least Busy Day:", cursor.fetchone())
import seaborn as sns

# Correlation Heatmap
plt.figure(figsize=(6,4))
sns.heatmap(df[['active_vehicles','trips','month','day']].corr(), annot=True, cmap='Blues')
plt.title("Correlation Between Variables")
plt.tight_layout()
plt.savefig("images/correlation_heatmap.png")
plt.show()
# Trips over time (line chart)
plt.figure(figsize=(10,4))
plt.plot(df['date'], df['trips'])
plt.xlabel("Date")
plt.ylabel("Trips")
plt.title("Uber Trips Over Time")
plt.tight_layout()
plt.savefig("images/trips_over_time_linechart.png")
plt.show()
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

# Machine Learning: Predict trips using active vehicles
X = df[['active_vehicles']]
y = df['trips']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)

print("\nML Model Score (accuracy):", model.score(X_test, y_test))
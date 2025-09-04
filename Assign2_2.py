import os
import pandas as pd
import numpy as np

# ---------- Helper Functions ----------
def load_all_data(folder="temperatures"):
    all_data = []
    for file in os.listdir(folder):
        if file.endswith(".csv"):
            filepath = os.path.join(folder, file)
            df = pd.read_csv(filepath)

            # Reshape wide format (months as columns) to long format
            df_long = df.melt(
                id_vars=["STATION_NAME"],
                value_vars=["January","February","March","April","May","June",
                            "July","August","September","October","November","December"],
                var_name="Month",
                value_name="Temperature"
            )
            all_data.append(df_long)

    return pd.concat(all_data, ignore_index=True)


def assign_season(month):
    summer = ["December", "January", "February"]
    autumn = ["March", "April", "May"]
    winter = ["June", "July", "August"]
    spring = ["September", "October", "November"]

    if month in summer:
        return "Summer"
    elif month in autumn:
        return "Autumn"
    elif month in winter:
        return "Winter"
    else:
        return "Spring"

# ---------- Task 1: Seasonal Average ----------
def seasonal_average(data):
    data = data.dropna(subset=["Temperature"])  # ignore missing values
    data["Season"] = data["Month"].apply(assign_season)

    seasonal_avg = data.groupby("Season")["Temperature"].mean()

    # Ensuring correct seasonal order
    season_order = ["Summer", "Autumn", "Winter", "Spring"]
    seasonal_avg = seasonal_avg.reindex(season_order)

    with open("average_temp.txt", "w") as f:
        for season, avg in seasonal_avg.items():
            f.write(f"{season}: {avg:.1f}°C\n")

# ---------- Task 2: Largest Temperature Range ----------
def largest_temp_range(data):
    data = data.dropna(subset=["Temperature"])  # drop NaN
    grouped = data.groupby("STATION_NAME")["Temperature"]

    ranges = grouped.max() - grouped.min()
    max_range = ranges.max()
    top_stations = ranges[ranges == max_range].index.sort_values()

    with open("largest_temp_range_station.txt", "w") as f:
        for station in top_stations:
            max_temp = grouped.max()[station]
            min_temp = grouped.min()[station]
            f.write(f"{station}: Range {max_range:.1f}°C (Max: {max_temp:.1f}°C, Min: {min_temp:.1f}°C)\n")

# ---------- Task 3: Temperature Stability ----------
def temperature_stability(data):
    data = data.dropna(subset=["Temperature"])  # drop NaN
    grouped = data.groupby("STATION_NAME")["Temperature"]

    stddevs = grouped.std()

    min_std = stddevs.min()
    max_std = stddevs.max()

    stable_stations = stddevs[stddevs == min_std].index.sort_values()
    variable_stations = stddevs[stddevs == max_std].index.sort_values()

    with open("temperature_stability_stations.txt", "w") as f:
        for s in stable_stations:
            f.write(f"Most Stable: {s}: StdDev {min_std:.1f}°C\n")
        for v in variable_stations:
            f.write(f"Most Variable: {v}: StdDev {max_std:.1f}°C\n")

# ---------- Main Program ----------
def main():
    data = load_all_data("temperatures")

    seasonal_average(data)
    largest_temp_range(data)
    temperature_stability(data)

    print("Analysis completed! Check the output text files.")

if __name__ == "__main__":
    main()
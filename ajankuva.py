import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Parse the given .csv file to a pandas dataframe and process some columns.
def create_df(file_path, year):
    df = pd.read_csv(file_path)
    
    df["aloitus"] = pd.to_datetime(df["aloitus"])
    df["lopetus"] = pd.to_datetime(df["lopetus"])
    df["kesto"] = df["lopetus"] - df["aloitus"]
    
    df[["päivämäärä"]] = df[["päivämäärä"]].apply(lambda x: pd.to_datetime(x + str(year), dayfirst=True))
    
    return df

def plot_active_minutes(df, year):    
    minutes_used = np.zeros(24*60)    
    
    df_mins = df[["aloitus", "lopetus"]]
    df_mins["aloitus"] = [60*t.hour + t.minute for t in df_mins["aloitus"]]
    df_mins["lopetus"] = [60*t.hour + t.minute for t in df_mins["lopetus"]]
    
    # Potentially slow, should be vectorized
    for idx, row in df_mins.iterrows():
        t1 = row["aloitus"]
        t2 = row["lopetus"]
        minutes_used[t1] += 0.5
        minutes_used[t2] += 0.5
        for i in range(t1+1, t2):
            minutes_used[i] += 1
    
    x_axis = np.arange(0, 24, 1/60)
    
    # Default resolution is low
    plt.figure(dpi=200)
    plt.title(f"Työskentelyn ajoittuminen {year}")
    ax = plt.gca()
    ax.set_xticks(range(0, 25, 2))
    ax.set_xticks(np.arange(0, 24, 0.5), minor=True)
    ax.grid(which="major")
    ax.grid(which="minor", alpha=0.3)
    plt.plot(x_axis, minutes_used)
    
def print_time_per_task(df):
    time_per_task = df.groupby("toiminta")[["kesto"]].sum()
    time_per_task = time_per_task.sort_values("kesto")
    time_per_task["tuntia"] = [dt.total_seconds() / 3600 for dt in time_per_task["kesto"]]
    
    print(time_per_task)
    print(time_per_task.sum())
    print("Työtunteja päivässä:", time_per_task.sum()["tuntia"] / 365)


def plot_daily_worktime(df, year):
    date = pd.to_datetime(f"01-01-{year}")
    timedelta = pd.to_datetime(f"02-01-{year}", dayfirst=True) - date
    zerodelta = date - date

    daily_worktime = df.groupby("päivämäärä")[["kesto"]].sum()["kesto"]
    while date < pd.to_datetime(f"01-01-{year+1}"):
        if date not in daily_worktime:
            daily_worktime[date] = zerodelta
        date += timedelta
    
    daily_worktime.sort_index(inplace=True)
    daily_worktime = daily_worktime.apply(lambda x: x.total_seconds() / 3600)

    weekly_worktime = daily_worktime.copy()
    
    week_timestamps = []
    weekly_average = []
    
    week_hours = 0
    start_timestamp = daily_worktime.index[0]
    numdays = 0
    for datetime in daily_worktime.index:
        numdays += 1
        week_hours += daily_worktime[datetime]
        if datetime.weekday() == 6:
            week_timestamps.append(start_timestamp)
            weekly_average.append(week_hours / numdays)
            numdays = 0
            week_hours = 0
        elif datetime.weekday() == 0:
            start_timestamp = datetime
    
    if numdays > 0:
        week_timestamps.append(start_timestamp)
        weekly_average.append(week_hours / numdays)
    
#    print(week_timestamps)
#    print(weekly_average)
    
    
    plt.figure(dpi=200)
    plt.title(f"Päivittäinen produktiivisuus {year}")
    plt.plot(daily_worktime)
#    print(daily_worktime)
    plt.step(week_timestamps, weekly_average, where="post")
    return daily_worktime

def get_stats(filepath, year):
    df = create_df(filepath, year)
    plot_active_minutes(df, year)
    print_time_per_task(df)
    return plot_daily_worktime(df, year)

get_stats("~/Desktop/ajat2021_utf8.csv", 2021)
get_stats("~/Desktop/ajat2022_utf8.csv", 2022)
get_stats("~/Desktop/ajat2023_utf8.csv", 2023)
plt.show()
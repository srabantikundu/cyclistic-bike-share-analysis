# Import required packages
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import datetime

months = [
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
]

def read_raw_data() :
    may_2020_df = pd.read_csv("../raw-data/202005-divvy-tripdata.csv")
    june_2020_df = pd.read_csv("../raw-data/202006-divvy-tripdata.csv")
    july_2020_df = pd.read_csv("../raw-data/202007-divvy-tripdata.csv")
    august_2020_df = pd.read_csv("../raw-data/202008-divvy-tripdata.csv")
    september_2020_df = pd.read_csv("../raw-data/202009-divvy-tripdata.csv")
    october_2020_df = pd.read_csv("../raw-data/202010-divvy-tripdata.csv")
    november_2020_df = pd.read_csv("../raw-data/202011-divvy-tripdata.csv")
    december_2020_df = pd.read_csv("../raw-data/202012-divvy-tripdata.csv")
    january_2021_df = pd.read_csv("../raw-data/202101-divvy-tripdata.csv")
    february_2021_df = pd.read_csv("../raw-data/202102-divvy-tripdata.csv")
    march_2021_df = pd.read_csv("../raw-data/202103-divvy-tripdata.csv")
    april_2021_df = pd.read_csv("../raw-data/202104-divvy-tripdata.csv")

    # Create a list of all dataframes

    frames = [
        may_2020_df,
        june_2020_df,
        july_2020_df,
        august_2020_df,
        september_2020_df,
        october_2020_df,
        november_2020_df,
        december_2020_df,
        january_2021_df,
        february_2021_df,
        march_2021_df,
        april_2021_df,
    ]

    return frames

def data_validation(frames):
    num_cols = []
    for frame in frames:
        if len(frame.columns) != 13 :
            raise NameError("Invalid number of columns")
    return num_cols

def clean_data_set(df):
    """
    Data cleaning
    a. Identify if we have columns and rows with missing data
    b. Investigate the first row with missing values further
    c. Find the sum of rows that contain null values
    d. Percentage of rows with missing values
    e. Drop rows with missing data. Most miss more than one missing value and account for 7.7% of the data.
    f. Lets not drop the columns as they have less than 5% missing values
    """

    #print(df.isnull().sum())
    #print(df[df.isnull().any(axis=1)])
    #print(df.iloc[800])

    sum_of_rows_with_null_values = df.isnull().any(axis=1).sum()
    #print(f"Total Null rows: {sum_of_rows_with_null_values}")

    perc_nan_rows = sum_of_rows_with_null_values / df.shape[0] * 100
    print(f"Percentage of null rows: {perc_nan_rows}")

    clean_df = df.dropna(axis="index")

    # Check if new df has any missing values
    # This step confirms that the data has no missing values
    #print(clean_df.isnull().sum())

    # Check if any ID's are duplicate
    #total_duplicate_rows = clean_df.duplicated().sum()
    #print(f"Duplicate rows: {total_duplicate_rows}")

    # Cleaned dataframe
    #print(clean_df)
    #print(clean_df.info())

    return clean_df

def processed_data_set(clean_df,df):
    """
    Process Data
        a. Transform started_at and ended_at into datetime
        b. Sort dataframe in descending order based on ended_at colum
        c. From above, we notice that the dataframe contains some data for June 2021.
        d. Create ride_length column (ride_length is in minutes)
        e. Remove negative ride_lengths
        
    """

    clean_df["started_at"] = pd.to_datetime(clean_df["started_at"])
    clean_df["ended_at"] = pd.to_datetime(clean_df["ended_at"])

    clean_df.sort_values(by=["ended_at"], inplace=True, ascending=False)

    june_2021_filter = df["ended_at"] <= "2021-06-03 00:00:00"
    clean_df = clean_df[june_2021_filter]

    ride_length = clean_df["ended_at"] - clean_df["started_at"]
    ride_length = np.round(ride_length.dt.total_seconds() / 60, 2)

    clean_df["ride_length"] = ride_length
    clean_df["day_of_week"] = clean_df["started_at"].dt.day_name()
    clean_df["month"] = pd.DatetimeIndex(clean_df["started_at"]).month
    clean_df["month_name"] = clean_df["started_at"].dt.strftime("%b")
    clean_df = clean_df[clean_df["ride_length"] > 0]

    print(clean_df)

    return clean_df

def plot_riders_per_category(processed_df):
     # Pie chart to show riders per category
    fig, ax = plt.subplots(figsize=(7, 3), dpi=90)
    labels = ["Member", "Casual"]
    total_riders = processed_df["member_casual"].value_counts()
    plt.pie(x=total_riders, autopct="%.1f%%", labels=labels)
    ax.set_title("Total Bike Hires Per Rider Category", pad=14, loc="center")
    plt.show()

def plot_bike_hires_per_month(processed_df):
    ride_hires_per_month = (
        processed_df["month"]
        .value_counts(sort=False)
        .rename_axis("Month")
        .reset_index(name="Total Hires")
    )

    print(ride_hires_per_month)

    plt.figure(figsize=(9, 5), dpi=150)
    plt.title("Total Bike Hires per Month", loc="left", pad=14)
    sns.barplot(data=ride_hires_per_month, x=months, y="Total Hires")
    plt.show()  

def plot_bike_hires_per_day_of_week(processed_df):
    ride_hires_per_day = (
        processed_df["day_of_week"]
        .value_counts()
        .rename_axis("Day")
        .reset_index(name="Total Hires")
    )
    ride_hires_per_day.sort_values(by=["Total Hires"], inplace=True, ascending=True)
    # print(ride_hires_per_day)

    plt.figure(figsize=(9, 5), dpi=150)
    plt.title("Total Bike Hires per Day of the Week", loc="left", pad=14)
    sns.barplot(data=ride_hires_per_day, x="Day", y="Total Hires")
    plt.show()

def plot_category_wise_riders_per_month(processed_df):
    monthly_bike_hires_per_customer_category = processed_df.groupby(["member_casual"])[
        "month_name"
    ].value_counts(sort=True)

    monthly_casual_member_df = pd.DataFrame()
    monthly_casual_member_df["casual"] = monthly_bike_hires_per_customer_category["casual"]
    monthly_casual_member_df["member"] = monthly_bike_hires_per_customer_category["member"]
    monthly_casual_member_df["Month"] = monthly_casual_member_df.index


    print(monthly_casual_member_df)

    pos = list(range(len(monthly_casual_member_df["casual"])))
    width = 0.25

    fig, ax = plt.subplots(figsize=(7, 3), dpi=90)

    plt.bar(pos, monthly_casual_member_df["casual"], width)
    plt.bar([p + width for p in pos], monthly_casual_member_df["member"], width)

    # Setting the y and x axis label
    ax.set_ylabel("Total Hires")
    ax.set_xlabel("Month")
    # Setting the chart's title
    ax.set_title("Total Bike Hires per Rider Category per Month", loc="left", pad=14)

    # Setting the position of the x ticks
    ax.set_xticks([p + 1.5 * width for p in pos])

    # Setting the labels for the x ticks
    ax.set_xticklabels(monthly_casual_member_df["Month"])

    # Adding the legend and showing the plot
    plt.legend(["Casual", "Member"], loc="upper right")
    plt.show()

def plot_category_riders_per_day(processed_df):
    bike_hires_per_customer_category = processed_df.groupby(["member_casual"])[
        "day_of_week"
    ].value_counts(sort=True)
    # print(bike_hires_per_customer_category)

    casual_member_df = pd.DataFrame()
    casual_member_df["casual"] = bike_hires_per_customer_category["casual"]
    casual_member_df["member"] = bike_hires_per_customer_category["member"]
    casual_member_df["Day"] = casual_member_df.index

    print(casual_member_df)

    pos = list(range(len(casual_member_df["casual"])))
    width = 0.25

    fig, ax = plt.subplots(figsize=(7, 3), dpi=90)

    plt.bar(pos, casual_member_df["casual"], width)
    plt.bar([p + width for p in pos], casual_member_df["member"], width)

    # Setting the y and x axis label
    ax.set_ylabel("Total Hires")
    ax.set_xlabel("Day of the Week")
    # Setting the chart's title
    ax.set_title("Total Bike Hires per Rider Category per Day", loc="left", pad=14)

    # Setting the position of the x ticks
    ax.set_xticks([p + 1.5 * width for p in pos])

    # Setting the labels for the x ticks
    ax.set_xticklabels(casual_member_df["Day"])

    # Adding the legend and showing the plot
    plt.legend(["Casual", "Member"], loc="upper right")
    plt.show()

def plot_avg_ride_length_by_category(processed_df):
    average_ride_length = processed_df.groupby(["member_casual"])["ride_length"].mean()
    # print(f"The average ride length per category {average_ride_length}")

    fig, ax = plt.subplots(figsize=(7, 3), dpi=90)
    labels = ["Casual", "Member"]
    plt.pie(x=average_ride_length, autopct="%.1f%%", labels=labels)
    ax.set_title("Average Ride Length", pad=14, loc="center")
    plt.show()

def plot_ride_length_day_of_week(processed_df):
    average_daily_ride_length = processed_df.groupby(["member_casual", "day_of_week"])[
        "ride_length"
    ].mean()
    
    weekly_average_ride_length_df = pd.DataFrame()

    weekly_average_ride_length_df["casual"] = average_daily_ride_length["casual"]
    weekly_average_ride_length_df["member"] = average_daily_ride_length["member"]
    weekly_average_ride_length_df["Day"] = weekly_average_ride_length_df.index

    pos = list(range(len(weekly_average_ride_length_df["casual"])))
    width = 0.25

    fig, ax = plt.figure(figsize=(9, 5), dpi=150)

    plt.bar(pos, weekly_average_ride_length_df["casual"], width)
    plt.bar([p + width for p in pos], weekly_average_ride_length_df["member"], width)

    # Setting the y and x axis label
    ax.set_ylabel("Average Ride Length")
    ax.set_xlabel("Day of the Week")
    # Setting the chart's title
    ax.set_title("Average Ride Length per Rider Category per Day", loc="left", pad=14)

    # Setting the position of the x ticks
    ax.set_xticks([p + 1.5 * width for p in pos])

    # Setting the labels for the x ticks
    ax.set_xticklabels(weekly_average_ride_length_df["Day"])

    # Adding the legend and showing the plot
    plt.legend(["Casual", "Member"], loc="upper right")
    plt.show()

def plot_rider_length_by_month(processed_df):
    average_daily_ride_length_per_month = processed_df.groupby(["member_casual", "month"])[
        "ride_length"
    ].mean()
    # print(f"Average ride lenth per category per day {average_daily_ride_length_per_month}")

    monthly_average_ride_length_df = pd.DataFrame()

    monthly_average_ride_length_df["casual"] = average_daily_ride_length_per_month["casual"]
    monthly_average_ride_length_df["member"] = average_daily_ride_length_per_month["member"]
    monthly_average_ride_length_df["month"] = monthly_average_ride_length_df.index

    # print(monthly_average_ride_length_df)

    pos = list(range(len(monthly_average_ride_length_df["casual"])))
    width = 0.25

    fig, ax = plt.figure(figsize=(9, 5), dpi=150)

    plt.bar(pos, monthly_average_ride_length_df["casual"], width)
    plt.bar([p + width for p in pos], monthly_average_ride_length_df["member"], width)

    # Setting the y and x axis label
    ax.set_ylabel("Average Ride Length")
    ax.set_xlabel("Month")
    # Setting the chart's title
    ax.set_title("Average Ride Length per Rider Category per Month", loc="left", pad=14)

    # Setting the position of the x ticks
    ax.set_xticks([p + 1.5 * width for p in pos])

    # Setting the labels for the x ticks
    ax.set_xticklabels(months)

    # Adding the legend and showing the plot
    plt.legend(["Casual", "Member"], loc="upper right")
    plt.show()

def main():
    # Read data into dataframes

    frames = read_raw_data()

    data_validation(frames)  

    # combine all the frames
    df = pd.concat(frames, axis=0, ignore_index=True)

    # Summary of the data
    #print(df.head(10))
    #print(df.info())

    clean_df = clean_data_set(df)
   
    processed_df = processed_data_set(clean_df,df)

    sns.color_palette("husl", 8)

    plot_riders_per_category(processed_df) 

    plot_bike_hires_per_month(processed_df)

    plot_bike_hires_per_day_of_week(processed_df)
    
    plot_category_wise_riders_per_month(processed_df)

    plot_category_riders_per_day(processed_df)

    plot_avg_ride_length_by_category(processed_df)

    plot_ride_length_day_of_week(processed_df)  

    plot_rider_length_by_month(processed_df)

if __name__ == "__main__":
    main()



import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chi': 'chicago.csv',
              'nyc': 'new_york_city.csv',
              'was': 'washington.csv' }


def get_filters():
    print('Hello! Let\'s explore some US bikeshare data!')
    #input the search data by user and limiting it to the current options
    while True:
        city = input("please choose the city:  \nfor 'chicago' enter 'CHI', 'new york city' enter 'NYC', 'washington' enter 'WAS': ").lower()
        if city in CITY_DATA:
            break
        else:
            print('enter a right city name')

    #limiting the input to the current options
    while True:
        month= input("select a month from the following:\n 'january', 'february', 'march', 'april', 'may', 'june' or 'all'. :" ).lower()
        if month in (['january', 'february', 'march', 'april', 'may', 'june','all']):
            break
        else:
            print("please make sure to pick either one of the above mentioned options")

    #limiting the input to the current options
    while True:
        day= input("please select the day you want or choose 'all'.: ").lower()
        if day in (['sunday','monday','tuesday','wednesday','thursday','friday','saturday','all']):
            break
        else:
            print("please make sure to pick either one of the following:sunday, monday, tuesday, wednesday, thursday, friday, or all")
    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    #reading the data from the chosen file by user
    df = pd.read_csv(CITY_DATA[city])

    #converting the srart time into datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    #month
    df['month'] = df['Start Time'].dt.month
    #week
    df['day_of_week'] = df['Start Time'].dt.day_name()
    #hour
    df['hour'] = df['Start Time'].dt.hour

    #incase the user choose a month not all:
    if month != 'all':
        #if filtering by month
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        df = df[df['month'] == month]

    if day != 'all':
        #filtering by selected day_of_week
        theDay = df[df['day_of_week'] == day.title()]
        return theDay
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    #calculating the most_common_month
    #mode() shows the most repeated number of the list, and [0] to pick only the value not the index in the df,series
    most_common_month = df['month'].mode()[0]
    print('the most common month is:', most_common_month)

    #calculating the most_common_day
    most_common_day= df['day_of_week'].mode()[0]
    print('most common day of the week is: ', most_common_day)

    #calculating the most_common_start_hour
    most_common_start_hour = df['hour'].mode()[0]
    print('And the most common start hour is:', most_common_start_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    #displaying the most common start station
    start_station = df['Start Station'].mode()[0]
    print('The most common start station is: ', start_station)

    # displaying the most common end station
    end_station = df['End Station'].mode()[0]
    print('The most common End station is: ', end_station)

    #displaying the most common end station
    most_common_grouped_stations =df.groupby(['Start Station','End Station']).size().sort_values().tail(1)
    print('The most common start and end station in the city is: ',most_common_grouped_stations)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    #displaying the total travel times
    total_travel_time = df['Trip Duration'].sum()
    print('The total travel time in seconds is:', total_travel_time)

    # display mean travel time
    mean_of_travel_time = df['Trip Duration'].mean()
    print('The mean of the travel time is: ', mean_of_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    count_of_user_type = df['User Type'].value_counts().to_frame()
    print('The count of User type is:\n', count_of_user_type)

    #  Display counts of gender

    try:
        gender_count= df['Gender'].value_counts().to_frame()
        print('The data sorted by gender: \n', gender_count)

        earliest_DOB_year=int( df['Birth Year'].min())
        recent_DOB_year = int(df['Birth Year'].max())
        common_DOB_year= int(df['Birth Year'].mode()[0])

        print('The earlier DOB year is; \n', earliest_DOB_year)
        print('The most recent DOB year is; \n', recent_DOB_year)
        print('The most common DOB year is; \n', common_DOB_year)

    except KeyError:
        print('sorry this data is not available in Washington')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def data_rows(city):
    print('Now after you determind the City, Month, Day...')
    answer = str(input("Your data is ready and it displays in bulck of 5 rowm, if you want to see the fist 5 rows \nType 'Y'for yes, 'N' for no")).lower()
    while answer not in ('y', 'n'):
        print("please type 'Y' or 'N'")
    moredata = 5
    while answer == 'y':
        try:
            for i in pd.read_csv(CITY_DATA[city],  chunksize= moredata):
                print(i)
                break
            question2 = input('To View the availbale raw in chuncks of 5 rows type: y\n').lower()
            if question2 == 'y':
                print('printing more data for you')
                moredata +=5
                continue
            else:
                print('Thank You')
                break
            break

        except KeyError:
            print('thanks')


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        data_rows(city)


        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
    main()

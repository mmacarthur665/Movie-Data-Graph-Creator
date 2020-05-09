"""
Program Name: Movie Data Graph Maker
Author: Michael Macarthur
Date: 5/9/2020

Summary: This program is intended to be fed the names of folders where movie data is retained. It will ask users
which movies they are interested in viewing information for. Based on which movies are specified by the user it will
show graphs of average rating by age group and % of responses in each age group by gender.
"""

# imports

import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import os
pd.set_option('display.max_columns', 1000)
pd.set_option('display.max_rows', 1000)
pd.set_option('display.width', 1000)


def pickMovieWithKeyword():
    """
    Function will ask users for where data lives and which movies they are interested in. It will create data structures
    with necessary information to feed the graphs that follow.
    :return: data structure with necessary data points for selected films
    """
    folder = input("Please enter the name of the folder with the data file:")  # obtains folder with data from user
    path = os.path.join(os.getcwd(), folder)  # sends program to that folder
    print("Plot1: ratings by age group")
    # first data frame with all relevant information for all possible movies
    df_all = pd.read_csv(path+'//'+'IMDB.csv', usecols=['Title', 'Genre1', 'Votes1829', 'Votes3044', 'Votes45A', 'VotesU18',
                                               'CVotesU18M', 'CVotesU18F', 'CVotes1829M', 'CVotes1829F', 'CVotes3044M',
                                               'CVotes3044F', 'CVotes45AM', 'CVotes45AF'])

    # data frame for movie selections - contains only titles
    df = pd.read_csv(path+'//'+'IMDB.csv', usecols=['Title'])

    # empty data frame to append user selections to
    user_movies = pd.DataFrame()

    df['Title2'] = df['Title'].str.lower()  # forces all titles to lower case
    tot_mov = str(len(df))  # total number of rows in data frame (AKA total number of movies)

    # asks user for how many movies they want to look at
    num_movies = eval(input("How many of the" + ' ' + tot_mov + ' ' + "movies would you like to consider? "))

    # counter for the while loop
    counter = 0

    # prints info for user
    print("Select", num_movies, "movies")
    print(" ")

    while counter < num_movies:  # while loop runs until we have entered the number of movies the user wanted to consider
        keyword = input("Enter movie keyword: ").lower()  # gets keyword from user
        df['indexes'] = df["Title2"].str.find(
            keyword)  # searches titles column, returns index of titles with keyword & stores in a column
        df_filt = df[df['indexes'] >= 0]  # filters on column of index numbers to where we found matches
        if len(df_filt) > 1:  # if we have more than 1 match
            df_filt = df_filt.drop(columns=['Title2', 'indexes'])  # dropps extra columns
            df_filt = df_filt.reset_index(drop=True)  # resets index to 0
            df_filt.index += 1  # forces index to start at 1 instead of zero
            print("Which of the following movies would you like to pick (enter a number) ")
            print(df_filt.to_string(index=True, header=False))  # prints all the options containing keyword
            user_selection = eval(input("enter a number: "))  # gets index for which movie they want
            movie = df_filt.loc[user_selection, :]  # finds movie title of movie they want
            user_movies = user_movies.append(movie)  # stores movie title in user_movies data frame
            counter += 1  # adds one to counter so we work towards ending the while loop
            print("Movie #", counter, ':',
                  movie.to_string(index=False, header=False))  # prints movie name and which number it is
            print('')
        elif len(df_filt) == 1:  # this section handles what we want when only one movie contains the keyword
            df_filt = df_filt.drop(columns=['Title2', 'indexes'])  # drops unnecessary columns
            df_filt = df_filt.reset_index(drop=True)  # resets index
            df_filt.index += 1  # forces index to start at 1
            movie = df_filt.loc[1, :]  # grabs title of movie
            user_movies = user_movies.append(movie)  # stores title of movie in data frame user_movies
            counter += 1  # adds 1 to counter
            print("Movie #", counter, ':', movie.to_string(index=False, header=False))
            continue
        else:  # this part handles when our search returns no movies b/c keyword doesnt exist
            print("Keyword is not in database. Please enter another.")  # asks user to try again
            continue

    print("-----------------------------------------------------------------------------------------")

    # Final data frame based on movies selected by the user with all other data points joined needed for future calcs
    df_forgraphs = pd.merge(user_movies, df_all, how="inner", on='Title')
    df_forgraphs['Genre1'] = '(' + df_forgraphs['Genre1'] + ')'  # adds parentheses
    df_forgraphs['Title_Genre'] = df_forgraphs['Title'] + df_forgraphs[
        'Genre1']  # concatenates title with genre for graphing labels

    return path, df_forgraphs

def plot1(df_forgraphs):
    """
    Function takes output of pickmovies function, manipulates data a bit, and produces line graph for selected films
    :return: line graph and saved line graph
    """

    df_plot1 = df_forgraphs.drop(columns=['Title', 'Genre1'])  # drops unnecessary columns
    df_plot1 = df_plot1.rename( # renames columns to what we want shown on the graph
        columns={'Votes1829': '18-29', 'Votes3044': '30-44', 'Votes45A': '>44', 'VotesU18': '<18'})
    df_plot1 = df_plot1[['Title_Genre', '<18', '18-29', '30-44', '>44']]

    df_plot1_transp = df_plot1.T  # flips rows and columns for easier graphing
    new_header = df_plot1_transp.iloc[0]  # fixes spacing issue with column headers
    df_plot1_transp.columns = new_header  # fixes spacing issue with column headers
    df_plot1_transp = df_plot1_transp.drop(['Title_Genre'])  # drops final unnecessary column

    # graphing stuff
    # plots line graph with dots and things
    plot1 = df_plot1_transp.plot(kind='line', title="Ratings by Age Group", legend=False, style='.-')
    plt.grid(color='lightgrey', linewidth=.5)  # sets grid color and line width
    plt.xlabel('Age_Group')  # sets x axis label
    plt.ylabel('Rating')  # sets y axis label
    plt.xticks(np.arange(4), df_plot1.columns[1:])  # arranges the x axis tick marks to align with labels
    # for loop will put movie titles at first point of every line
    for line, name in zip(plot1.lines, df_plot1['Title_Genre'].iloc[0:]):
        y = line.get_ydata()[0]  # gets y coordinate for first point on line
        x = line.get_xdata()[0]  # gets x coordinate for first point on line
        plt.annotate(name, xy=(x, y), color=line.get_color())  # places movie titles as annotations and color codes
    plt.savefig('plot1.png', dpi = 1000)
    plt.close()
    #plt.show()  #shows graph

def plot2(path):
    """
    function takes user input for ONE movies and returns a graph showing % of raters by gender-age group. Saves graph.
    :return: bar graph and saved copy of bar graph
    """
    num_movies2 = 1  # set to one b/c we only want this loop to run once
    counter2 = 0  # serves to break while loop
    user_movies2 = pd.DataFrame()  # empty dataframe
    # data frame for movie selections - contains only titles
    df = pd.read_csv(path + '//' + 'IMDB.csv', usecols=['Title'])
    df_all = pd.read_csv(path + '//' + 'IMDB.csv',
                         usecols=['Title', 'Genre1', 'Votes1829', 'Votes3044', 'Votes45A', 'VotesU18',
                                  'CVotesU18M', 'CVotesU18F', 'CVotes1829M', 'CVotes1829F', 'CVotes3044M',
                                  'CVotes3044F', 'CVotes45AM', 'CVotes45AF'])
    df['Title2'] = df['Title'].str.lower()  # forces all titles to lower case
    while counter2 < num_movies2:  # while loop runs until we have entered the number of movies the user wanted to consider
        keyword = input("Enter movie keyword: ").lower()  # gets keyword from user
        df['indexes'] = df["Title2"].str.find(
            keyword)  # searches titles column, returns index of titles with keyword & stores in a column
        df_filt = df[df['indexes'] >= 0]  # filters on column of index numbers to where we found matches
        if len(df_filt) > 1:  # if we have more than 1 match
            df_filt = df_filt.drop(columns=['Title2', 'indexes'])  # dropps extra columns
            df_filt = df_filt.reset_index(drop=True)  # resets index to 0
            df_filt.index += 1  # forces index to start at 1 instead of zero
            print("Which of the following movies would you like to pick (enter a number) ")
            print(df_filt.to_string(index=True, header=False))  # prints all the options containing keyword
            user_selection = eval(input("enter a number: "))  # gets index for which movie they want
            movie = df_filt.loc[user_selection, :]  # finds movie title of movie they want
            user_movies2 = user_movies2.append(movie)  # stores movie title in user_movies data frame
            counter2 += 1  # adds one to counter so we work towards ending the while loop
            print("Movie #", counter2, ':',
                  movie.to_string(index=False, header=False))  # prints movie name and which number it is
            print('')
        elif len(df_filt) == 1:  # this section handles what we want when only one movie contains the keyword
            df_filt = df_filt.drop(columns=['Title2', 'indexes'])  # drops unnecessary columns
            df_filt = df_filt.reset_index(drop=True)  # resets index
            df_filt.index += 1  # forces index to start at 1
            movie = df_filt.loc[1, :]  # grabs title of movie
            user_movies2 = user_movies2.append(movie)  # stores title of movie in data frame user_movies
            counter2 += 1  # adds 1 to counter
            print("Movie #", counter2, ':', movie.to_string(index=False, header=False))
            continue
        else:  # this part handles when our search returns no movies b/c keyword doesnt exist
            print("Keyword is not in database. Please enter another.")  # asks user to try again
            continue

    df_forgraphs2 = pd.merge(user_movies2, df_all, how="inner", on='Title')  # joins all movie data to selected
    df_plot2 = df_forgraphs2[['Title', 'CVotes1829F', 'CVotes1829M', 'CVotes3044F', 'CVotes3044M',
                              'CVotes45AF', 'CVotes45AM', 'CVotesU18F', 'CVotesU18M']]  # picks certain columns
    title = df_plot2.Title.astype(str)  # stores title of movie for future use in graph
    df_plot2 = df_plot2.drop(columns=['Title']) # drops columns we dont need anymore
    df_plot2['tot_votes'] = df_plot2.sum(axis=1)  # calculates total votes
    df_plot2 = df_plot2.rename(columns={'CVotes1829F': '18-29F', 'CVotes1829M': '18-29M', 'CVotes3044F': '30-44F',
                                        'CVotes3044M': '30-44M', 'CVotes45AF': '>44F', 'CVotes45AM': '>44M',
                                        'CVotesU18F': '<18F', 'CVotesU18M': '<18M'})  # renames columns
    df_plot3 = df_plot2[['18-29F', '18-29M', '30-44F', '30-44M', '>44F', '>44M', '<18F', '<18M']].div(
        df_plot2.tot_votes, axis=0)  # calcs % of gender-age group
    df_plot3 = df_plot3[['<18F', '18-29F', '30-44F', '>44F', '<18M', '18-29M', '30-44M', '>44M']]  # re-orders cols
    percents = df_plot3.iloc[0, :] * 100  # expresses %s without % sign
    percents = pd.DataFrame(percents)  # puts percents into a data frame
    ypos = np.arange(len(percents.index))  # sets up axes
    percent_lst = round(percents[0], 2).tolist()  # puts rounded %s into list
    string = "%"  # % sign for adding to list in next line
    p_labels = ["{}{}".format(i, string) for i in percent_lst]  # creates labels to use on bars
    labels = percents.index.tolist()  # creates list of labels
    plt.bar(ypos, percent_lst, align='center',  # creates bar chart and colors appropriately
            color=['purple', 'purple', 'purple', 'purple', 'green', 'green', 'green', 'green'], label=percent_lst)
    plt.grid(False)  # removes grid lines
    plt.xticks(ypos, labels, rotation=30)  # creates xticks as desired and rotates them 30 degrees
    plt.title('Percentage of raters within gender-age group for {}'.format(''.join(map(str, title))))  # title of graph
    plt.ylabel('% of raters')   # y-axis label

    for i in range(len(ypos)):
        plt.text(x=ypos[i], y=percent_lst[i], s=p_labels[i],
                 ha='center', va='baseline')  # loop creates the individual bar labels
    plt.savefig('plot2.png', dpi = 1000)  # saves plot to working directory
    plt.close()  # closes the graph
    #plt.show()

def main():
    """
    function serves to call other functions
    :return: nothing
    """

    path, df_forgraphs = pickMovieWithKeyword()  # calls pickmovie function and assigns what it returns
    plot1(df_forgraphs=df_forgraphs)  # creates plot 1 with data returned by previous function
    print('Plot2: Percentage of raters within gender-age. Select a movie:')  # prints required line
    plot2(path=path)  # creates plot 2 based on data in the path variable

main()
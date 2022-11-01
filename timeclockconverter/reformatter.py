import numpy as np
import pandas as pd


def make(filepath):
    """
    Calls a series of functions that read CSV into pandas.DataFrame,
    aggregate the hours of each employee into one row per employee,
    and reformats DataFrame to match Paylocity format.

    :param filepath: pathlib.Path type of target filepath
    :return df: fully converted pandas.DataFrame
    """
    if filepath.suffix == '.csv':  # reads csv
        df = reindex_cols(
                aggregate_rows(
                    read_file(filepath)))
        return df
    else:
        raise Exception('in converter.make(), not csv')


def read_file(filepath):
    """
    Reads CSV file into pandas.DataFrame, ignores header and footers from
    NewAccess download.
    Only reads in employee IDs, department number, pay rate, and hours columns.

    :param filepath: pathlib.Path type of target filepath
    :return: df: pandas.DataFrame with relevant columns
    """
    df = pd.read_csv(filepath,
                     names=['id', 'dept', 'rate', 'hours'],
                     usecols=[2, 7, 6, 5],
                     skiprows=3,
                     skipfooter=14)
    return df


def aggregate_rows(df):
    """
    Groups DataFrame df by employee IDs. If an employee ID appears more than
    once, the employee's hours are summed and aggregated into a single row.

    :param df: pathlib.Path type of target filepath
    :return: newdf: DataFrame with aggregated hours
    """
    # define how to aggregate various columns
    agg_funcs = {'hours': 'sum', 'rate': 'first', 'dept': 'first'}

    # create new DataFrame, combining hours of rows with same ID
    newdf = df.groupby(df['id']).aggregate(agg_funcs)
    return newdf


def reindex_cols(df):

    df['E'] = 'E'
    df['REG'] = 'REG'
    df['nan1'] = np.nan
    df['nan2'] = np.nan
    order = ['E', 'REG', 'hours', 'nan1', 'rate', 'nan2', 'dept']
    df = df.reindex(columns=order)
    return df


def get_department(df):
    """
    Should only be called on fully converted DataFrame.
    Gets department number of df. Used by FileFactory to rename
    output file by department.

    :param df: pathlib.Path type of target filepath
    :return: df.iat[0,6]: should correspond to the department #
    :raises: Exception: if file is empty -> no department #
    """
    try:
        return df.iat[0, 6]
    except Exception as e:
        raise Exception('empty unconverted file detected, please remove')  # rethrows to Dialog

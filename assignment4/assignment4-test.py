import pytest
import pandas as pd
from assignment4.assignment4 import task1_data_frame, task1_with_salary, task1_older

def test_task1_dataframe_creation():
    assert isinstance(task1_data_frame, pd.DataFrame)
    assert list(task1_data_frame.columns) == ['Name', 'Age', 'City']
    assert len(task1_data_frame) == 3

def test_salary_column_added():
    assert 'Salary' in task1_with_salary.columns
    assert all(task1_with_salary['Salary'] == [70000, 80000, 90000])

def test_age_increment():
    assert all(task1_older['Age'] == task1_data_frame['Age'] + 1)

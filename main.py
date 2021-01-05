# This is a sample Python script.
from src import twitterService

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

concurentAccount = '@BarackObama'

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    twitterService.writeTwitterInfo(screen_name=concurentAccount)
    twitterService.createGraph(screen_name=concurentAccount)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/

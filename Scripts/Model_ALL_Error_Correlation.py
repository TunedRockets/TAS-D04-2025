

import Handling_ALL_Functions
import pandas as pd

def join_data(frame1:pd.DataFrame, frame2:pd.DataFrame, desync)-> pd.DataFrame:
    '''
    joins the two dataframe columnwise from a given desync time\n
    I.e. shifts frame two BACKWARDS by the desync.
    '''

    # frame 2 we want to shift:

    




def main():
    
    # get the data:
    data_LS = Handling_ALL_Functions.get_processed_data(1, "LS")
    print(data_LS)







if __name__ == "__main__":
    main()



import Handling_ALL_Functions
import pandas as pd
import numpy as np

def join_data(frame1:pd.DataFrame, frame2:pd.DataFrame, desync)-> pd.DataFrame:
    '''
    joins the two dataframe columnwise from a given desync time\n
    I.e. shifts frame two BACKWARDS by the desync.\n
    assumes time is at index 0 in the rows
    '''

    # info on frames
    shape_1 = frame1.shape
    shape_2 = frame2.shape

    # the shape of the joined is going to be the min of the row and the combined of the columns
    # minus one because time is shared
    columns = shape_1[1] + shape_2[1] - 1
    rows = min(shape_1[0], shape_2[0])

    joined = np.empty((rows, columns))

    #set which frame is the guiding one:
    if shape_1[0] > shape_2[0]: # guiding is which one that guides the join process
        guide = frame2
        follower = frame1
    else:
        guide = frame1
        follower = frame2 # python is by reference so this shouldn't be slow
    
    try:
        i_f = 0 # follower index
        for i in range(len(guide)):
            # combine them 
            time = guide.iloc[i][0] # the time of the timestamp

            # put in guide data
            for j in range(0, guide.shape[1]):
                joined[i][j] = guide.iloc[i][j]

            # now find the corresponding data in the follower
            while follower.iloc[i_f][0] < time: # TODO, set this to closest, not just first above
                i_f += 1
                # might break if index goes out of range...
            # continues until it's passed the right point.
            # i_f is now at the follower just beyond the time data
            for j in range(1, follower.shape[1]-1):
                joined[i][j + guide.shape[1]] = follower.iloc[i_f][j+1] # puts it in the row after the guide
    except IndexError:
        # we probably ran out of datapoints in the follower :(
        # but that's fine
        pass

    joined = pd.DataFrame(joined)
    # gets rid of the metadata, so let's reintroduce it
    joined.columns = ["time", "temp1", "temp2", "temp3", "temp4"]  

    return joined

def main():


    
    # Generating random test data
    np.random.seed(42) 
    data_size = 100  

    data1 = pd.DataFrame({
        'time': range(data_size),
        'error_something': np.random.uniform(0.01, 0.02, data_size),
        'error_IV': np.random.uniform(0.01, 0.02, data_size)})

    data_size = 80
    data2 = pd.DataFrame({
        'time': range(0, 2*data_size, 2),
        'error_one': np.random.uniform(0.01, 0.02, data_size),
        'error_B': np.random.uniform(0.01, 0.02, data_size),})

    joined_data = join_data(data1, data2, 4)



    
    # # get the data:
    # data_LS = Handling_ALL_Functions.get_processed_data(1, "LS")
    print(joined_data)







if __name__ == "__main__":
    main()

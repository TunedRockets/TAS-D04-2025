

import Handling_ALL_Functions
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import itertools

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

            if abs(follower.iloc[i_f-1][0] - time) < abs(follower.iloc[i_f][0] - time):
                i_f -= 1
            # picks the closest one


            for j in range(1, follower.shape[1]-1):
                joined[i][j + guide.shape[1]] = follower.iloc[i_f][j+1] # puts it in the row after the guide
    except IndexError:
        # we probably ran out of datapoints in the follower :(
        # but that's fine
        pass

    joined = pd.DataFrame(joined)
    # gets rid of the metadata, so let's reintroduce it
    fol_col_names = follower.columns
    guide_col_names = guide.columns
    col_names = set(fol_col_names).union(set(guide_col_names)) # hope this keeps order?
    # if not then change this
    joined.columns = list(col_names)  

    return joined

def least_squares_regression(x, y):
    """
    Performs least squares regression on two lists of error values.
    
    Parameters:
    x (list of float): Independent variable.
    y (list of float): Dependent variable.
    
    Returns:
    tuple: (slope, intercept) of the regression line.
    """
    x = np.array(x)
    y = np.array(y)
    A = np.vstack([x, np.ones(len(x))]).T
    slope, intercept = np.linalg.lstsq(A, y, rcond=None)[0]
    return slope, intercept

def plot_errors(error1, error2, error3, error4, error5, error6):
    """
    Takes in 6 lists and generates a single plot with subplots for each combination of error types,
    including least squares regression lines.
    
    Parameters:
    error1, error2, error3, error4, error5, error6 (list of float): Lists of error values.
    """
    errors = [error1, error2, error3, error4, error5, error6]
    
    if any(len(errors[0]) != len(err) for err in errors):
        raise ValueError("All error lists must have the same length.")
    
    combinations = list(itertools.combinations(range(6), 2))
    num_plots = len(combinations)
    cols = 3
    rows = (num_plots + cols - 1) // cols
    
    fig, axes = plt.subplots(rows, cols, figsize=(15, 10))
    axes = axes.flatten()
    
    for idx, (i, j) in enumerate(combinations):
        x = errors[i]
        y = errors[j]
        slope, intercept = least_squares_regression(x, y)
        
        axes[idx].scatter(x, y, color='b', alpha=0.7, edgecolors='k', label="Data")
        axes[idx].set_xlabel(f"Error {i+1}")
        axes[idx].set_ylabel(f"Error {j+1}")
        axes[idx].set_title(f"Error {i+1} vs Error {j+1}")
        
        # Plot regression line
        x_vals = np.linspace(min(x), max(x), 100)
        y_vals = slope * x_vals + intercept
        axes[idx].plot(x_vals, y_vals, color='r', linestyle='--', label="Regression Line")
        
        axes[idx].grid(True, linestyle='--', alpha=0.6)
        axes[idx].legend()
    
    for idx in range(num_plots, len(axes)):
        fig.delaxes(axes[idx])
    
    plt.tight_layout()
    plt.show()

# Example usage
error1 = [1.2, 2.4, 3.1, 4.7, 5.5]
error2 = [2.1, 3.9, 3.0, 5.1, 4.8]
error3 = [1.5, 2.7, 3.2, 4.5, 5.0]
error4 = [2.3, 3.1, 3.8, 4.9, 5.7]
error5 = [1.8, 2.9, 3.4, 4.8, 5.6]
error6 = [2.0, 3.5, 3.9, 5.2, 5.9]

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

    plot_errors(error1, error2, error3, error4, error5, error6)
    
    # # get the data:
    # data_LS = Handling_ALL_Functions.get_processed_data(1, "LS")
    print(joined_data)







if __name__ == "__main__":
    main()

#TODO

import sys
import os
sys.path.insert(0, os.path.abspath('TAS-D04-2025\Translating-Data-Required-Format'))
import data_handler 

def main():
    
    # get the data:
    data_LS = data_handler.get_processed_data(1, "LS")
    print(data_LS)







if __name__ == "__main__":
    main()

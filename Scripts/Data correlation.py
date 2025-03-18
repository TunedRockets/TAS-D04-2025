#TODO
import sys
import os
sys.path.insert(0, os.path.abspath('TAS-D04-2025'))
sys.path.insert(0, os.path.abspath('TAS-D04-2025\Data-and-Data-Handling\Translating-Data-Required-Format'))
import Scripts.constants as constants
import data_handler
# does this work?



def main():
    
    # get the data:
    data_LS = data_handler.get_processed_data(1, "LS")
    print(data_LS)







if __name__ == "__main__":
    main()

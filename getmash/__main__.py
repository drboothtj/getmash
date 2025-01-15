'''
Main entry point for getmash
    functions: entrypoint()
'''

from datetime import datetime
from getmash import main

def entrypoint():
    '''
    Entry point for getmash
    '''
    try:
        start_time = datetime.now()
        main.main()
        end_time = datetime.now()
        run_time = end_time - start_time
        #print('Thank you for using getmash. The analysis took %s', run_time)
    except Exception as e:
        print(e)
        exit(1)
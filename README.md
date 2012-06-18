# Schmap API Client 

## Installation
Clone this project, make sure you have setuptools installed and then run,

python setup.py test

(sudo) python setup.py install

## Usage
Look at examples directory for the usage.


Basically there are 4 schmap API calls. This python api is a wrapper for these calls 

get_status - gets the status of a request
analyze_account - Analyze the followers of a given twitter account
analyze_list    - Analyze the list of twitter handles. The return values can be full_analysis ( aggregated counts)
                  or profiled_dataset ( individual counts)
get_dataset     - Use this call to get the processed data after calling analyze_list with profiled_dataset
get_analysis    - Use this call to get the processed data after calling analyze_list with full_analysis
 


# Bulk Extraction (above 10 million rows and more) from remote databases
This Program extracts huge volumes of data using distributed programming `(ray - clustering technique)` and its performance depends on available `Machine CPU Cores and its Threads`.

## Introduction
- This Appplication helps in parallely fetching data from remote databases using ray-clustering where `pandas` and native mtehods may take huge time or can even possibly fail.

- Other Areas where we can use this approach is training ML Models, retrieving daat from such trained models etc.

- Here we are using some random `employee` table data whch we created using data_generation_scripts.py and inserted into our mariadb  database(SQL Database).
  
- You can directly import sample_data.sql file into employee_info table on your local databse if you want to test.

- This main purpose of this app is to explain steps in properly utilizing ray clstering and to understand distributed programming works  , you can always change below file content to fit your extraction requirements
  -   database_acess.py (all query logic is here)

## How to Setup and Run

- Install required dependencies using below command 
```
pip install -r requirements.txt

ray start --head 

```
- 
- Now run `python app.py` and program will start fetching data and assigns individual data extracts to each worker and finally exports data into specified files as per config.

- In brower head over to `http://127.0.0.1:8265` where you can find `Ray dashboard` where your job is running on multiple workers(threads) and you can also perform certains actions through UI.

<img width="1680" alt="Screenshot 2024-02-04 at 12 45 17 PM" src="https://github.com/sodekiranavinash/Bulk-Extract-Pandas-Ray-Clustering/assets/86816437/16a13ba1-306d-40bd-be89-4e7b2257d85f">


## Note
- When running on local database, this program actually takes more time as local databases are fast to featch and doesnt have any overheads, so recommend to test on remote databases.

## Performance
- For example if 1 million records take 15 minutes on pandas or native sql conector methods, our approach can handle 7 million in the same time (assuming you have 8 hreads CPU, 1 thread to keep program alive)
- based on CPU threads , some workers tasks can go in queue but still it will be faster than our conventional approach.


## How to contributions
- Anybody who can abtract the app into some template structure for web scraping google is always welcomed.

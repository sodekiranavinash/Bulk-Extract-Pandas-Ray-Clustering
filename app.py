import time
import ray
import pandas as pd
from database_access import DatabaseAccess
from data_processor import DataProcessor
from data_writer import DataWriter
from constants import constants

# Initialize Ray
ray.init()

if __name__ == '__main__':
    
    db_access : DatabaseAccess = DatabaseAccess()
    '''you can uncommnet this code to find time taken for single query fetch,
    but is only beneficial if your connecting to cloud databases, 
    running local will not help as fetching from local db will be always be faster'''
    # all_fetch_start_time = time.time()
    # all_records = db_access.fetch_all_records(constants.DB_TABLE)
    # file_name = "All_Data.csv"
    # DataWriter.write_file(all_records,f"{constants.OUTPUT_FILE_PATH}{file_name}")
    # print(f"Total Time Taken for fetching by traditional method : {time.time() - all_fetch_start_time}")

    data_frame_count  = db_access.get_data_length(constants.DB_TABLE) # checking total extract size
    if data_frame_count is None:
        print("Error: Failed to retrieve data length from the database.")
    if data_frame_count <= 0:
        print("Please Add some data into table for extraction")
        exit()

    # print(f"total records count : {data_frame_count}")

    max_rows_per_worker : int = data_frame_count // constants.MAX_CPU_CORES if data_frame_count > constants.MAX_PANDAS_FETCH else data_frame_count // constants.AVG_CPU_CORES
    fetch_chunk_size : int = DataProcessor.calculate_chunk_size(data_frame_count, max_rows_per_worker)
    batch_size : int = data_frame_count // fetch_chunk_size
    num_batches : int = data_frame_count // batch_size
    # print(f"no of batches : {num_batches} & batch size {batch_size}")

    # adding jobs to ray cluster
    ray_fetch_start_time = time.time()
    tasks = []
    

    for i in range(num_batches):
        start_row : int = i * constants.MAX_ROWS_PER_FILE + 1
        end_row : int = (i + 1) * constants.MAX_ROWS_PER_FILE
        task = db_access.fetch_records.remote(
                        constants.DB_TABLE,
                        start_row=start_row, 
                        end_row=end_row
                        )
        tasks.append(task)

    if records := list(ray.get(tasks)):
        data_frame : pd.DataFrame = pd.concat(records, axis=0, ignore_index=True)
        # print(f"Total Time Taken to fetch data using ray clustering: {time.time() - ray_fetch_start_time}")

        no_of_chunks, chunk_size = DataProcessor.get_chunk_details(len(data_frame), constants.MAX_ROWS_PER_FILE)
        # print(f"-----------------chunk size :{chunk_size} no of chunks {no_of_chunks}---------------------------------")

        lower_chunk_size : int = 0
        higher_chunk_size : int = chunk_size

        for index, value in enumerate(range(no_of_chunks)):
            
            chunk_data = data_frame[lower_chunk_size: higher_chunk_size]
            output_file = f"bulk_extract{index}.csv"
            DataWriter.write_file(chunk_data, f"{constants.OUTPUT_FILE_PATH}{output_file}")
            
            lower_chunk_size = higher_chunk_size
            higher_chunk_size = higher_chunk_size + chunk_size

    print(f"Program completed file creation and please check output folder: {constants.OUTPUT_FILE_PATH}")

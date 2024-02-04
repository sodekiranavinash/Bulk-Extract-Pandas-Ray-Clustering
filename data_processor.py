class DataProcessor:
    @staticmethod
    def get_chunk_details(length_of_data, max_rows_per_file) -> tuple:
        try:
            chunk_size_value = DataProcessor.calculate_chunk_size(length_of_data, max_rows_per_file)
            chunk_size = int(length_of_data / chunk_size_value)
            no_of_chunks, remainder = divmod(length_of_data, chunk_size)
            if remainder > 0:
                no_of_chunks += 1
            return (no_of_chunks, chunk_size)
        except ZeroDivisionError as e:
            print(f"Error calculating chunk details: {e}")
            return (0, 0)

    @staticmethod
    def calculate_chunk_size(data_size, max_chunk_size) -> int:
        try:
            if data_size <= max_chunk_size:
                return 1
            chunk_size = data_size // (max_chunk_size - 1)
            chunk_size += (data_size % (max_chunk_size - 1) > 0)
            return chunk_size
        except ZeroDivisionError as e:
            print(f"Error calculating chunk size: {e}")
            return 0

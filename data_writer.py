
class DataWriter:
    @staticmethod
    def write_file(data_frame, output_file) -> None:
        try:
            data_frame.to_csv(output_file, index=False)
        except Exception as e:
            print(f"Error writing CSV file: {e}")


import matlab.engine

# Start MATLAB engine
eng = matlab.engine.start_matlab()

# Define paths for input and output Excel files
input_excel_path = 'input_data.xlsx'
output_excel_path = 'output_data.xlsx'

# Call the MATLAB function
eng.process_excel(input_excel_path, output_excel_path, nargout=0)

# Stop MATLAB engine
eng.quit()

# You can now read the output Excel file using pandas, if needed
output_df = pd.read_excel(output_excel_path)
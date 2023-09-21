# Creating_Video_from_Image_Frames
# Application Overview:

This Python script is designed to create a video from a collection of image frames stored in a MySQL database and referenced in a JSON file. It allows the user to specify a timestamp and duration to select a range of frames from the database and compile them into a video. Below is a detailed explanation of the key components and functionalities of the application:

# 1. Logger Setup:

The application starts by configuring a logging system. Any errors encountered during its execution will be logged in a file named error.log.
# 2. User Input:

The user is prompted to provide two pieces of input:<br>
timestamp_input: A timestamp in the format YYYY-MM-DD HH:MM:SS.<br>
duration_input: The duration of the video in seconds.<br>
# 3. Database Configuration:

The database connection parameters (host, user, password, and database name) are defined in the db_config dictionary.<br>
# 4. get_batches Function:

This function retrieves batches of frames from the MySQL database based on the provided timestamp and duration.<br>
It calculates an ending timestamp by adding the duration to the input timestamp.<br>
SQL query is executed to select batches within the specified time range.<br>
# 5. gather_frames Function:

This function gathers frame information from a JSON file (frame_info.json) based on the batch information.<br>
It reads each line from the JSON file, extracts frame information, and appends frames that fall within the specified batch's frame ID range.<br>
# 6. Frame Compilation and Video Creation:

The script iterates through the retrieved batches and gathers frames using the gather_frames function.<br>
Frames are sorted by frame_id.<br>
The width and height of the video are determined from the first frame, and default values are used if no frames are found.<br>
A video writer is initialized using OpenCV, and frames are sequentially added to create the final video.<br>
Any errors encountered while writing frames to the video are logged.<br>
# 7. Output:

Upon successful video creation, a message is displayed, indicating that the video has been created as output_video.mp4.<br>
# Usage Instructions:

Run the script in a Python environment.<br>
Provide the requested input: timestamp and duration.<br>
The script will compile the frames from the specified time range and create a video named output_video.mp4.<br>
**Note**: Ensure that the MySQL database and JSON file (frame_info.json) are properly configured and contain the required data for this script to work correctly also all the necessary library are installed.<br>

This documentation aims to provide a comprehensive understanding of the application's purpose and functionality for both developers and users. It explains the key functions, their roles, and the expected input and output of the application.

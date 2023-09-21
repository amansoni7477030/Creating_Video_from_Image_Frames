import cv2
import json
import mysql.connector
from datetime import datetime
from datetime import timedelta
import logging

# Initialize the logger
logging.basicConfig(filename='error.log', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

# User input
timestamp_input = input("Enter TIMESTAMP (YYYY-MM-DD HH:MM:SS): ")
duration_input = int(input("Enter DURATION OF VIDEO (in seconds): "))

# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '12345678',
    'database': 'aman',
}

# Function to retrieve batch information
def get_batches(timestamp, duration):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Calculate ending timestamp based on duration
        ending_timestamp = (datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S') +
                            timedelta(seconds=duration)).strftime('%Y-%m-%d %H:%M:%S')

        # Query to retrieve batches within the specified time range
        query = """
            SELECT * FROM batches
            WHERE timestamp BETWEEN %s AND %s
        """
        cursor.execute(query, (timestamp, ending_timestamp))
        batches = cursor.fetchall()

        connection.close()
        return batches
    except Exception as e:
        logging.error(f"Error retrieving batches: {str(e)}")
        return []

# Function to gather frame information from JSON file
def gather_frames(batch_info):
    frames = []

    try:
        with open('frame_info.json', 'r') as json_file:
            for line in json_file:
                frame_info = json.loads(line)
                frame_id = frame_info['frame_id']

                if batch_info[1] <= frame_id <= batch_info[2]:  # Access tuple elements by index
                    frames.append(frame_info)
    except Exception as e:
        logging.error(f"Error gathering frames: {str(e)}")

    return frames

# Create a list of frames for the specified time range
batches = get_batches(timestamp_input, duration_input)
all_frames = []

for batch_info in batches:
    frames = gather_frames(batch_info)
    all_frames.extend(frames)

# Sort frames by frame_id
all_frames.sort(key=lambda x: x['frame_id'])

# Initialize width and height with default values
width = 640  # Default width
height = 480  # Default height

# Calculate width and height from the first frame if frames are found
if all_frames:
    first_frame_path = all_frames[0]['image_path']
    if first_frame_path:
        first_frame = cv2.imread(first_frame_path)
        height, width, _ = first_frame.shape

# Create a video from gathered frames
output_video = cv2.VideoWriter('output_video.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 25, (width, height))

for frame_info in all_frames:
    image_path = frame_info['image_path']
    if image_path:
        try:
            frame = cv2.imread(image_path)
            output_video.write(frame)
        except Exception as e:
            logging.error(f"Error writing frame to video: {str(e)}")

output_video.release()
print("Video created successfully: output_video.mp4")

import os
from concurrent.futures import ThreadPoolExecutor
from moviepy.editor import VideoFileClip, ColorClip, concatenate_videoclips

def parse_meta_file(meta_file):
    timestamps = []
    with open(meta_file, 'r') as file:
        for line in file:
            start_time, end_time, title = line.strip().split('-')
            timestamps.append((start_time.strip(), end_time.strip(), title.strip()))
    return timestamps

def convert_to_seconds(time_str):
    hours, minutes, seconds = map(int, time_str.split(':'))
    return hours * 3600 + minutes * 60 + seconds

def add_intro(video_clip, intro_clip_path, duration=0, fade_duration=1):
    intro = VideoFileClip(intro_clip_path).subclip(0, duration)
    
    # Get the resolution of the original video clip
    resolution = video_clip.size
    
    # Resize the intro to match the video's resolution while maintaining aspect ratio
    intro = intro.resize(height=resolution[1])
    
    # Set the duration of the intro clip
    if duration != 0:
        intro = intro.set_duration(duration)
    
    # Fade in the intro clip
    intro = intro.crossfadein(fade_duration)
    
    # Concatenate the intro clip with the video clip
    final_clip = concatenate_videoclips([intro, video_clip], method="compose")
    return final_clip

def process_chapter(video_file, intro_clip, start_time, end_time, title):
    video = VideoFileClip(video_file)
    start_seconds = convert_to_seconds(start_time)
    end_seconds = convert_to_seconds(end_time)
    
    # Extract the video chapter
    chapter_clip = video.subclip(start_seconds, end_seconds)
    
    # Add intro to the chapter clip
    chapter_clip = add_intro(chapter_clip, intro_clip)
    
    # Create the folder if it doesn't exist
    folder_name = os.path.splitext(video_file)[0]
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    
    # Write the final video to file inside the folder
    output_file = os.path.join(folder_name, f"{title}.mp4")
    try:
        chapter_clip.write_videofile(output_file, codec="libx264")
        print(f"Chapter '{title}' created: {output_file}")
    except Exception as e:
        print(f"Error creating chapter '{title}': {e}")

def split_video(video_file, intro_clip, timestamps):
    with ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(process_chapter, video_file, intro_clip, start_time, end_time, title)
            for start_time, end_time, title in timestamps
        ]
        for future in futures:
            try:
                future.result()  # Wait for all threads to complete
            except Exception as e:
                print(f"Error in future result: {e}")

if __name__ == "__main__":
    intro_clip = "intro.mp4"
    video_file = "video.mp4"
    meta_file = "meta.txt"
    timestamps = parse_meta_file(meta_file)
    
    split_video(video_file, intro_clip, timestamps)

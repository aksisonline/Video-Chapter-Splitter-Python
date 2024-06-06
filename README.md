# Video Chapter Splitter

This Python application splits a video into chapters based on timestamps provided in a metadata file. It also adds an intro clip to each chapter.

## Setup

1. Install the necessary dependencies by running the `setup.py` script:

```sh
python setup.py install
```

2. Place your video file and intro clip in the project root directory. The video file should be named `video.mp4` and the intro clip should be named `intro.mp4`.

3. Create a `meta.txt` file in the project root directory. This file should contain the timestamps and titles for each chapter in the following format:

```txt
00:00:00-00:00:10-Chapter1
00:00:10-00:00:20-Chapter2
00:00:20-00:00:30-Chapter3
```

Each line represents a chapter. The first timestamp is the start time, the second timestamp is the end time, and the text after the second hyphen is the chapter title.

## Usage

Run the `app.py` script:

```sh
python app.py
```

The script will create a new folder with the same name as your video file. Each chapter will be saved as a separate `.mp4` file in this folder.

## Dependencies

- moviepy
```


### Project by AKS
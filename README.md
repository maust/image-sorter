# image-sorter
[![Build Status](https://travis-ci.org/maust/image-sorter.svg?branch=master)](https://travis-ci.org/maust/image-sorter)
[![Coverage Status](https://img.shields.io/coveralls/maust/image-sorter.svg)](https://coveralls.io/r/maust/image-sorter?branch=master)

A python script python script to sort
* pictures into folders by their date and 
* recognize pictures which are part of the same panorama to put them into subfolders

It moves image files from a *source directory* to a *target directory* depending on when the photo was taken, using EXIF data and creation date as a fallback.

Furthermore it tries to recognize image files which are part of a panorama picture, therefore the following criteria are used as of now:
* the pictures are taken in Manual mode (EXIF ExposureProgram)
* the time between each picture of a panorama is less than 5 seconds (EXIF DateTimeOriginal)
* the ISO doesn't change (EXIF ISOSpeedRatings)
* the aperture doesn't change (EXIF FNumber)
* the shutter speed doesn't change (EXIF ExposureTime)

Limitations:
* The source folder must not have subfolders.
* As of now there has to be always a JPG for each CR2 (-> RAW+L ; only RAW not supported yet).
* The current implementation doesn't identify panoramas taken with compact cameras (as most of them use panorama mode and not manual mode).

The naming of the directories follow a simple naming convention 
* YYYY-MM-DD for the first level
* Panorama X with X starting with 1 as subdirectories 

The result looks somewhat like this:
```
├── 2013-01-11
│   ├── Panorama 1
│   │   ├── IMAGE_5019.jpg
│   │   ├── IMAGE_5020.jpg
│   │   ├── IMAGE_5021.jpg
│   │   ├── IMAGE_5022.jpg
│   │   ├── IMAGE_5023.jpg
│   │   ├── IMAGE_5024.jpg
│   │   ├── IMAGE_5025.jpg
│   │   ├── IMAGE_5026.jpg
│   ├── Panorama 2
│   |   ├─ ...
│   └── ...
├── 2014-12-23
│   ├── IMAGE_9124.jpg
│   ├── IMAGE_9235.jpg
│   ├── IMAGE_9236.jpg
│   └── IMAGE_9237.jpg
├── ...
```

## Run

Sort images from `src_dir` into `dest_dir`.

    $ python sorter.py src_dir dest_dir

# image-sorter
[![Build Status](https://travis-ci.org/maust/image-sorter.svg?branch=master)](https://travis-ci.org/maust/image-sorter)
[![Coverage Status](https://img.shields.io/coveralls/maust/image-sorter.svg)](https://coveralls.io/r/maust/image-sorter?branch=master)

A python script python script to sort
* pictures into folders by their date and 
* recognize pictures which are part of the same panorama to put them into subfolders

## Detailed description

It moves image files from a *source directory* to a *target directory* depending on when the photo was taken, using EXIF data and creation date as a fallback.

Furthermore it tries to recognize image files which are part of a panorama picture, therefore the following criteria are used as of now:
* the pictures are taken in Manual mode (EXIF ExposureProgram)
* the time between each picture of a panorama is less than 5 seconds (EXIF DateTimeOriginal)
* the ISO doesn't change (EXIF ISOSpeedRatings)
* the aperture doesn't change (EXIF FNumber)
* the shutter speed doesn't change (EXIF ExposureTime)

If the directory of the date (e.g. '2013-01-11') or a directory with an additional suffix after the date (e.g. '2013-01-11 Berlin') already exists at the *target directory* the files will be moved into it.

Limitations:
* The source folder must not have subfolders.
* As of now only CR2 files are supported (and movies)
* The current implementation doesn't identify panoramas taken with compact cameras (as most of them use panorama mode and not manual mode).

The naming of the directories follow a simple naming convention 
* YYYY-MM-DD for the first level
* Panorama X with X starting with 1 as subdirectories 

The result looks somewhat like this:
```
├── 2013-01-11
│   ├── Panorama 1
│   │   ├── IMAGE_5019.cr2
│   │   ├── IMAGE_5020.cr2
│   │   ├── IMAGE_5021.cr2
│   │   ├── IMAGE_5022.cr2
│   │   ├── IMAGE_5023.cr2
│   │   ├── IMAGE_5024.cr2
│   │   ├── IMAGE_5025.cr2
│   │   ├── IMAGE_5026.cr2
│   ├── Panorama 2
│   |   ├─ ...
│   └── ...
├── 2014-12-23
│   ├── IMAGE_9124.cr2
│   ├── IMAGE_9235.cr2
│   ├── IMAGE_9236.cr2
│   └── IMAGE_9237.cr2
├── ...
```

## Run

Sort images from `src_dir` into `dest_dir`.

    $ python sorter.py src_dir dest_dir

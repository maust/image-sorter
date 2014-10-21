#!/usr/bin/env python

import os
import datetime
from datetime import timedelta
from os import walk
import shutil
import sys

import exifread


def get_exif_datetime_string(tags):
    if 'EXIF DateTimeOriginal' in tags:
        return str(tags['EXIF DateTimeOriginal'])
    elif 'EXIF DateTimeDigitized' in tags:
        return str(tags['EXIF DateTimeDigitized'])
    return None


def get_date(path, tags):
    return get_datetime(path, tags).date()


def get_datetime(path, tags):
    exif_date = get_exif_datetime_string(tags)
    if exif_date:
        return datetime.datetime.strptime(exif_date, '%Y:%m:%d %H:%M:%S')
    return file_creation_date(path)


def file_creation_date(path):
    """
    Use mtime as creation date because ctime returns the
    the time when the file's inode was last modified; which is
    wrong and almost always later.

    """
    mtime = os.path.getmtime(path)
    return datetime.datetime.fromtimestamp(mtime)


def fulfill_panorama_criterias(path1, path2, pic1_tags, pic2_tags):
    # TODO Manual works as criteria only with DSLR, most compact cameras use panorama mode
    if str(pic1_tags.get('EXIF ExposureProgram')) != "Manual":
        return False
    if str(pic2_tags.get('EXIF ExposureProgram')) != "Manual":
        return False
    if str(pic1_tags.get('EXIF ExposureTime')) != \
            str(pic2_tags.get('EXIF ExposureTime')):
        return False
    if str(pic1_tags.get('EXIF ISOSpeedRatings')) != str(pic2_tags.get('EXIF ISOSpeedRatings')):
        return False
    print(pic1_tags.get('EXIF ISOSpeedRatings'))
    if str(pic1_tags.get('EXIF FNumber')) != str(pic2_tags.get('EXIF FNumber')):
        return False
    date1 = get_datetime(path1, pic1_tags)
    date2 = get_datetime(path2, pic2_tags)
    if (date2 - date1) > timedelta(seconds=5):
        return False
    return True


def similar_folder_exists(dest_folder, date):
    for (_, dirs, _) in os.walk(dest_folder):
        for x in dirs:
            if date == x[:10]:
                return x
    return date


def get_folder(dest_folder, date):
    if not os.path.exists(dest_folder):
        return dest_folder + date + '/'
    elif os.path.exists(dest_folder + date + '/'):
        return dest_folder + date + '/'
    return dest_folder + similar_folder_exists(dest_folder, date) + '/'


def analyze_pictures(src_folder, dest_folder, pictures):
    prevpic = None
    curpath = None
    curtags = None
    filedic = {}
    cr2s = []
    curpanorama = []
    count = 0
    date_of_previous_panorama = None

    for pic in pictures:
        print(pic)
        if os.path.splitext(pic)[1].lower() == ".cr2":
            cr2s.append(pic)
        if os.path.splitext(pic)[1].lower() in ['.jpg', '.jpeg', '.png', '.mov']:
            # Get File and ExifTags
            curpath = src_folder + pic
            with open(curpath, 'rb') as cf:
                curtags = exifread.process_file(cf, details=False)
            # Calculate Subfolder
            filedic[pic] = get_folder(dest_folder,
                                      get_date(curpath, curtags).isoformat())
            if prevpic is not None:
                prevpath = src_folder + prevpic
                with open(prevpath, 'rb') as pf:
                    prevtags = exifread.process_file(pf, details=False)

                if fulfill_panorama_criterias(prevpath, curpath, prevtags, curtags):
                    if len(curpanorama) == 0:
                        curpanorama.append(prevpic)
                    curpanorama.append(pic)

                elif len(curpanorama) > 0:
                    # Just finished a panorama
                    if date_of_previous_panorama and not date_of_previous_panorama == get_date(prevpath, prevtags):
                        count = 0

                    count += 1
                    for x in curpanorama:
                        filedic[x] = filedic[x] + "Panorama " + str(count) + "/"

                    curpanorama = []
                    date_of_previous_panorama = get_date(prevpath, prevtags)
            prevpic = pic

    # If last picture was part of panorama
    if len(curpanorama) > 0:
        if not date_of_previous_panorama == get_date(curpath, curtags):
            count = 0
        count += 1
        for x in curpanorama:
            filedic[x] = filedic[x] + "Panorama " + str(count) + "/"

    # There has to be a JPG for each CR2 (-> RAW+L ; only RAW not supported yet)
    for x in cr2s:
        tmp = x.rsplit('.', 1)[0] + '.JPG'
        filedic[x] = filedic[tmp]

    return filedic


def parse_args(argv):
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('src_folder')
    parser.add_argument('dest_folder')
    return parser.parse_args(argv[1:])


def get_files(mypath):
    f = []
    for (_, _, files) in walk(mypath):
        f.extend(files)
    return f


def run(src_folder, dest_folder):
    if not (src_folder.endswith('/')):
        src_folder += '/'
    if not (dest_folder.endswith('/')):
        dest_folder += '/'
    if not os.path.exists(src_folder):
        return 0
    pictures = get_files(src_folder)
    sorted_file_dic = analyze_pictures(src_folder, dest_folder, pictures)
    for pic in sorted_file_dic:
        dest = sorted_file_dic[pic]
        if not os.path.exists(dest):
            print("Destination path {0} does not exist. Creating now...".format(dest))
            os.makedirs(dest)
        print("Moving {0} to {1} ...".format(pic, dest))
        shutil.move(src_folder + pic, dest)


def main(argv):
    args = parse_args(argv)
    run(args.src_folder, args.dest_folder)
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))

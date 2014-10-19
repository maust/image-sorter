"""
Unit tests for sorter.py

Run with:
$ py.test -f sorter_test.py -v

"""

import unittest

import exifread

import sorter


class ExifTests(unittest.TestCase):
    def test_fulfillPanoramaCriterias1(self):
        path1 = 'test_files/IMG_5627.JPG'
        pic1 = open(path1, 'rb')
        pic1_tags = exifread.process_file(pic1, details=False)
        path2 = 'test_files/IMG_5628.JPG'
        pic2 = open(path2, 'rb')
        pic2_tags = exifread.process_file(pic2, details=False)
        case = sorter.fulfill_panorama_criterias(path1, path2, pic1_tags, pic2_tags)
        self.assertTrue(case)

    def test_fulfillPanoramaCriterias2(self):
        path1 = 'test_files/P1140437.JPG'
        pic1 = open(path1, 'rb')
        pic1_tags = exifread.process_file(pic1, details=False)
        path2 = 'test_files/P1140438.JPG'
        path2 = 'test_files/P1140438.JPG'
        pic2 = open(path2, 'rb')
        pic2_tags = exifread.process_file(pic2, details=False)
        case = sorter.fulfill_panorama_criterias(path1, path2, pic1_tags, pic2_tags)
        # TODO Fix identification of panoramas with compact cameras
        # self.assertTrue(case)

    def test_NotfulfillPanoramaCriterias1(self):
        path1 = 'test_files/P1010003.JPG'
        pic1 = open(path1, 'rb')
        pic1_tags = exifread.process_file(pic1, details=False)
        path2 = 'test_files/P1010004.JPG'
        pic2 = open(path2, 'rb')
        pic2_tags = exifread.process_file(pic2, details=False)
        case = sorter.fulfill_panorama_criterias(path1, path2, pic1_tags, pic2_tags)
        # TODO Fix identification of panoramas with compact cameras
        # self.assertFalse(case)


class ScriptTests(unittest.TestCase):
    def test_parse_args(self):
        args = sorter.parse_args('sorter.py src/ dest/'.split())
        self.assertEqual(args.src_folder, 'src/')
        self.assertEqual(args.dest_folder, 'dest/')

"""
ADanayi
The sorter class
This is a class which does the sorting...
This is so Good!
"""

import os
import shutil
import rarfile
import zipfile
import re

__author = "Abolfal Danayi"

movie_ext_list = ['mpg', 'mpeg', 'avi', 'mov', 'wmv', 'asx', \
                 'wma', 'asf', 'm4v', 'mkv', 'asf', 'mp2', 'mp4']

audio_ext_list = ['mp3', 'm3u', 'm3u8', 'pls', 'cda', 'flac', 'mid', \
                  'midi', 'acc', 'm4a', 'wav', 'acc', 'ogg', 'wpl']

image_ext_list = ['jpg', 'jpeg', 'png', 'bmp', 'tif', 'tiff', 'gif', \
                  'psd', 'raw', 'ico']

docs_ext_list = ['docx', 'doc', 'pdf', 'txt', 'rtf', 'docm', 'wps',\
                 'xls', 'xlsx', 'xlsm', 'ppt', 'csv', 'htm', 'html', 'xml', 'mht',\
                 'mhtml', 'xps']


class Sorter:
    def __init__(self, unsorted_path, sort_into_path):
        self.spath = unsorted_path
        self.dpath = sort_into_path
        self.check = False
        if not os.path.exists(self.spath):
            print ("There is no path...")
        else:
            self.check = True
        if self.check:
            print(self.dpath)
            if os.path.exists(self.dpath):
                shutil.rmtree(self.dpath)
            self.Video = os.path.join(sort_into_path, "Videos")
            self.Audio = os.path.join(sort_into_path, "Audios")
            self.Image = os.path.join(sort_into_path, "Images")
            self.Doc = os.path.join(sort_into_path,   "Documents")
            self.Other = os.path.join(sort_into_path, "Others")
            self.Comp = os.path.join(sort_into_path,  "Compressed")
            if self.check:
                os.mkdir(sort_into_path)
                self.log = open(os.path.join(sort_into_path, "log.txt"), 'w')
                self.log.write("Easy file Arrange!\n")
                self.log.write("Made by ADanayi!\n")
                self.log.write("Please send me feedback if you find this app useful!\n")
                self.log.write("ADanayidet@gmail.com\n")
                self.log.write("----------------------------------------------------\n")
                os.mkdir(self.Video)
                os.mkdir(self.Audio)
                os.mkdir(self.Doc)
                os.mkdir(self.Other)
                os.mkdir(self.Image)
                os.mkdir(self.Comp)

    def sort(self):
        if not self.check:
            return False
        files = self.find_all_files(self.spath)
        for file in files:
            ext = self.ext(file)
            self.log.write("-----------------\n")
            self.log.write("File: {} -> Ext: {}\n".format(file, ext))
            if ext:
                if ext in movie_ext_list:
                    adr = self.check_ext_folder(ext, self.Video)
                    self.write_file(file, adr)
                elif ext in audio_ext_list:
                    self.log.write("is Audio\n")
                    adr = self.check_ext_folder(ext, self.Audio)
                    self.write_file(file, adr)
                elif ext in docs_ext_list:
                    self.log.write("is Doc\n")
                    adr = self.check_ext_folder(ext, self.Doc)
                    self.write_file(file, adr)
                elif ext in image_ext_list:
                    self.log.write("is Image\n")
                    adr = self.check_ext_folder(ext, self.Image)
                    self.write_file(file, adr)
                elif ext == 'zip':
                    self.log.write("is Zip\n")
                    if self.zip_ok(file):
                        adr = self.check_ext_folder(ext, self.Other)
                        self.write_file(file, adr)
                    else:
                        self.log.write("Archive is empty\n")
                elif ext == 'rar':
                    self.log.write("is Rar\n")
                    if self.rar_ok(file):
                        adr = self.check_ext_folder(ext, self.Other)
                        self.write_file(file, adr)
                    else:
                        self.log.write("archive is empty\n")
            else:
                print("with no extention\n")
                self.write_file(file, adr)

    @staticmethod
    def find_all_files(tree_path):
        files_list = []
        all_list = os.listdir(tree_path)
        for name in all_list:
            adr = os.path.join(tree_path, name)
            if os.path.isfile(adr):
                files_list.append(adr)
            else:
                new_tree = adr
                files_list.extend(Sorter.find_all_files(new_tree))
        return files_list

    @staticmethod
    def ext(file_adr):
        RE = re.compile(r'.*\.(.*?)$')
        matches = RE.match(file_adr)
        if matches:
            return matches.groups()[0]
        else:
            return False

    @staticmethod
    def rar_ok(file_adr):
        RF = rarfile.RarFile(file_adr)
        if RF.namelist() == []:
            return False
        else:
            return True

    @staticmethod
    def zip_ok(file_adr):
        RF = zipfile.ZipFile(file_adr)
        if RF.namelist() == []:
            return False
        else:
            return True

    @staticmethod
    def check_ext_folder(ext, folder):
        temp = os.path.join(folder, ext)
        if not os.path.exists(temp):
            os.mkdir(temp)
        return temp

    @staticmethod
    def write_file(file, adr):
        i = 0
        file_dir = ['file', 'dir']
        path = adr
        Sorter.get_file(file, file_dir)
        name = file_dir[1]
        n_name = name
        n_adr = os.path.join(path, name)
        while os.path.exists(n_adr):
            i += 1
            n_name = str(i) + "_" + name
            n_adr = os.path.join(path, n_name)
        print(n_adr)
        shutil.copy(file, n_adr)
        return True

    @staticmethod
    def get_file(file, seperated):
        sep = os.path.sep
        if sep == "\\":
            sep = "\\\\"
        pattern = r'(.*' + sep + r')(.*?)$'
        re_check = re.compile(pattern)
        ans = re_check.match(file)
        seperated[0] = ans.groups()[0]
        seperated[1] = ans.groups()[1]


    def __del__(self):
        if self.check:
            self.log.close()

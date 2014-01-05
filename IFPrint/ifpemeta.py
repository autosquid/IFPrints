#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#   Author  :   uuplusu
#   E-mail  :   justin.seeley.cn@gmail.com
#   Date    :   14/01/05 17:46:05
#   Desc    :
#
import os
import hashlib

hashlen = 8


def shorten(x):
    return str(int(hashlib.new('md5', x).hexdigest(), 16) % (10 ** hashlen))


def getprintsingle(f, hashed=True):
    filestat = os.stat(f)
    meta = [os.path.abspath(f),  # absolute file name
            filestat.st_size,  # file size
            filestat.st_mtime,  # time of modification
            filestat.st_ctime  # time of creation
            ]
    fullinfo = ''.join([str(s) for s in meta])
    return shorten(fullinfo) if hashed else fullinfo


def _checkexistance(imglist):
    existance = map(os.path.exists, imglist)
    return all(existance)


def getprintlist(imglist, hashed=True):
    if not _checkexistance(imglist):
        raise Exception
    metas = ''.join([getprintsingle(fn, False) for fn in imglist])
    return shorten(metas) if hashed else metas


def isimage(filename):
    return os.path.splitext(filename)[1].lower() in ['.jpg', '.bmp', '.png']


def getprintdir(abspath, recursive=False, hashed=True):
    if not recursive:
        allfiles = os.listdir(abspath)
        allimsfn = filter(isimage, allfiles)
        allimsfullfn = [os.path.join(abspath, s) for s in allimsfn]
        return getprintlist(allimsfullfn, hashed)

    lists = []
    for path, _, filenames in os.walk(abspath):
        lists += [os.path.join(path, s) for s in filter(isimage, filenames)]

    return getprintlist(lists, hashed)


if __name__ == '__main__':
    fn = '../data/residule_A41.png'
    listfn = ['../data/residule_A41.png',
              '../data/residule_A42.png']
    pathname = '../data/d1'
    print 'single file:', getprintsingle(fn)
    print 'filelist:', getprintlist(listfn)
    print 'recursive dir', getprintdir(pathname, True)
    print 'nonrecursive dir', getprintdir(pathname, False)

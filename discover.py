#!/usr/bin/env python

import os,fnmatch,sys
if os.path.isdir("/usr/local/lib/python2.7/dist-packages/") and "/usr/local/lib/python2.7/dist-packages/" not in sys.path:
    sys.path.append("/usr/local/lib/python2.7/dist-packages/")
import requests,re,pprint,guessit

COMMON_VIDEO_FILE_FORMATS = ['webm','mkv','flv','vob','ogg','ogv','drc','mng','avi','mov','qt','wmv','yuv','rm','rmvb','asf','mp4','m4p','m4v','mpg','mp2','mpeg','mpe','mpv','m2v','m4v','svi','3gp','3g2','mxf','roq','nsv','arf','dv4','h264','mp2v','m4e','ogm','moov','3gp2','wm','movie','mpeg1','dat','k3g','3gpp','ogv','ivf','mk3d','avc','trec']
COMMON_SUBTITLES_FILE_FORMATS = ['*.srt','*.sub','*.ssa','*.subtitle']
pp = pprint.PrettyPrinter(indent=1)

def find(source_directory, files=True, dirs=True, hidden=False, relative=True, topdown=True):
    source_directory = os.path.join(source_directory, '')
    for parent, ldirs, lfiles in os.walk(source_directory, topdown=topdown):
        if relative:
            parent = parent[len(source_directory):]
        if dirs and parent:
            yield os.path.join(parent, '')
        if not hidden:
            lfiles   = [nm for nm in lfiles if not nm.startswith('.')]
            ldirs[:] = [nm for nm in ldirs  if not nm.startswith('.')]
            ldirs.sort()
        if files:
            lfiles.sort()
            for nm in lfiles:
                nm = os.path.join(parent, nm)
                yield nm

def find_filetype_in_directory(directory, patterns):
    for root, dirs, files in os.walk(directory):
        for basename in files:
            if len(filter(lambda x: fnmatch.fnmatch(basename.lower(),x),patterns)):
                filename = os.path.join(root, basename)
                yield filename

def scan(source_directory):
    dictionary = {}
    filenames = []
    for file_path in find(source_directory, dirs=False, relative=False):
        file_name = os.path.basename(file_path)
        video_extension = file_path.split(".")[-1].lower()
        if (not re.match('sample',file_name,re.I)) and (video_extension in COMMON_VIDEO_FILE_FORMATS):
            directory = os.path.abspath(os.path.join(file_path, os.pardir))
            guess = guessit.guess_file_info(file_path, info=['filename'])
            subtitles = []
            for subtitle_file in find_filetype_in_directory(directory,COMMON_SUBTITLES_FILE_FORMATS):
                subtitles.append(subtitle_file)
            dictionary[re.sub("\W+","",file_name.lower())] = {
                                                                'directory': directory, 
                                                                'file_path': file_path, 
                                                                'video_extension' : video_extension,
                                                                'title': str(guess['title']) if guess.has_key('title') else 'Unknown',
                                                                'screenSize': str(guess['screenSize']) if guess.has_key('screenSize') else 'Unknown',
                                                                'format': str(guess['format']) if guess.has_key('format') else 'Unknown',
                                                                'year': str(guess['year']) if guess.has_key('year') else 'Unknown',
                                                                'videoCodec': str(guess['videoCodec']) if guess.has_key('videoCodec') else 'Unknown',
                                                                'video_extension_parsed': str(guess['container']) if guess.has_key('container') else 'Unknown',
                                                                'subtitles_files' : subtitles
                                                            }
            filenames.append(file_name)
        else:
            continue
    pp.pprint(dictionary)

if __name__ == "__main__":
    if sys.argv[1] == 'scan':
        scan(sys.argv[2])        
    elif sys.argv[1] == 'organize':
        #organize(*sys.argv[2:])
        print "Nothing to do yet!"
    else:
        print "Nothing to do!"

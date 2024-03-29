import os
import random
import shutil
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

organiser = r"C:\Users\admin\Desktop\ORGANISED"
desktop = r"C:\Users\admin\Desktop"
downloads = r"C:\Users\admin\Downloads"
documents = r"C:\Users\admin\Documents"
dist = r"C:\Users\admin\dist"

pics = r"C:\Users\admin\Desktop\ORGANISED\PICS"
docs = r"C:\Users\admin\Desktop\ORGANISED\DOCS"
exe = r"C:\Users\admin\Desktop\ORGANISED\EXE"
music = r"C:\Users\admin\Desktop\ORGANISED\COOL MUSIC"
videos = r"C:\Users\admin\Desktop\ORGANISED\VIDEOS"
folders = r"C:\Users\admin\Desktop\ORGANISED\FOLDERS"

myFiles = [pics, docs, exe, music, videos,folders]

docEnds = (
'.doc', '.docx', '.pptx', '.pptm', '.ppt', '.pdf', '.xps', '.potx', '.potm', '.pot', '.thmx', '.ppsx', '.ppsm', '.pps',
'.ppam', '.ppa', '.xml','.txt')
picEnds = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.tiff','.webp')
videoEnds = ('.mpg', '.mov', '.wmv', '.rm', '.flv', '.mkv', '.mp4', '.avi', '.MP4')
exeEnds = ('.exe', '.EXE','.zip','.ZIP')
musicEnds = ('.mp3', '.aac', '.wav', '.flac', '.ogg', '.wma', '.m4a', '.mid','.MP3')

downloaded = os.listdir(downloads)
onDesktop = os.listdir(desktop)

picsList = os.listdir(pics)


if not os.path.exists(organiser):
 os.makedirs(organiser)

else:
 for file in myFiles:
     if not os.path.exists(file):
         os.makedirs(file)


def isInUse(path):

 while True:
     try:
      size = os.path.getsize(path)

     except Exception:
      size = 0

     time.sleep(1)

     try:
         newSize = os.path.getsize(path)

     except Exception:
         newSize = 0

     if(size == newSize):
        break

def moveItems(itemPath):
    try:
        fileName = os.path.split(itemPath)[1]
        newPath = itemPath

        if fileName.lower().endswith(docEnds):
            newPath = os.path.join(docs, fileName)

        elif fileName.lower().endswith(picEnds):
           newPath = os.path.join(pics, fileName)

        elif fileName.lower().endswith(videoEnds):
           newPath = os.path.join(videos, fileName)

        elif fileName.lower().endswith(exeEnds):
            newPath = os.path.join(exe, fileName)

        elif fileName.lower().endswith(musicEnds):
            newPath = os.path.join(music, fileName)

        elif os.path.isdir(itemPath):
            newPath = os.path.join(folders, fileName)

        while os.path.exists(newPath):
            num = random.randrange(0, 600)
            dirPath, filePath = os.path.split(newPath)
            filePath = str(num) + filePath
            newPath = os.path.join(dirPath, filePath)


        shutil.move(itemPath, newPath)


    except shutil.Error:
       pass

    except Exception:
        pass


class observeDesktop(FileSystemEventHandler):

    def on_any_event(self, event):

        if event.is_directory:
            if event.event_type == 'created':
                isInUse(event.src_path)
                moveItems(event.src_path)

        if event.event_type == 'created':
            isInUse(event.src_path)
            moveItems(event.src_path)



if __name__ == '__main__':

    if len(downloaded) > 0:
     for items in downloaded:
        moveItems(os.path.join(downloads,items))


    for items in onDesktop:

     if items.lower().endswith(picEnds):
         moveItems(os.path.join(desktop, items))

     if items.lower().endswith(docEnds):
         moveItems(os.path.join(desktop, items))

     if items.lower().endswith(videoEnds):
         moveItems(os.path.join(desktop, items))

     if items.lower().endswith(musicEnds):
         moveItems(os.path.join(desktop, items))


    observingDesktop = observeDesktop()


    observer1 = Observer()

    observer1.schedule(observingDesktop, desktop, recursive=False)

    observer1.start()


    try:
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        observer1.stop()


    observer1.join()



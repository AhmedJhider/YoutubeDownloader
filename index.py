import requests
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QApplication , QFileDialog
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QUrl, QSize
from pytube import YouTube

def commas(x):
    ch=str(x)
    k=3
    while len(str(x))>3:
        ch=ch[:len(ch)-k]+","+ch[len(ch)-k:]
        x=x//1000
        k=k+4
    return ch

def length(x):
    ch=""
    h=str(x//3600)
    x=x%3600
    m=str(x//60)
    s=str(x%60)
    zt = lambda x:"0"+x if len(x)==1 else x
    return h+":"+zt(m)+":"+zt(s)
def search():
    windows.w1.hide()
    windows.w2.hide()
    windows.t.hide()
    try:
        yt = YouTube(windows.l1.text())
        if "?sqb" in yt.thumbnail_url:
            url = yt.thumbnail_url[:yt.thumbnail_url.find("?sqp")]
        else:
            url = yt.thumbnail_url

        response = requests.get(url)
        windows.l3.setText(str(yt.title)+"\n\n"+str(length(yt.length)+" | "+str(commas(yt.views)))+" views")
        data = response.content
        pixmap = QPixmap() 
        pixmap.loadFromData(data)
        windows.l2.setPixmap(pixmap)

        windows.l4.show()
        windows.b2.show()
        windows.b3.show()
    except:
        windows.w1.show()
         
def location():
    windows.w1.hide()
    if windows.l1.text()!="":
        directory = QFileDialog.getExistingDirectory(None, "Select Directory", "", QFileDialog.ShowDirsOnly)
        windows.l4.setText(directory)
    else:
        windows.w1.show()

def on_progress(stream, chunk, bytes_remaining):
    ts = stream.filesize
    sd = ts - bytes_remaining
    rts = round(ts/1000000,1)
    rsd = round(sd/1000000,1)
    windows.t.setText(str(rsd)+" MB/ "+str(rts)+" MB")
    QApplication.processEvents()
def on_complete(stream, file_path):
    windows.waiting.hide()
    windows.complete.show()
    windows.t.setText(str(round(YouTube(windows.l1.text()).streams.get_by_resolution("720p").filesize/1000000,1))+" MB/ "+str(round(YouTube(windows.l1.text()).streams.get_by_resolution("720p").filesize/1000000,1))+" MB")

def download():
    windows.w2.hide()
    if windows.l4.text()!="":
        try:
            yt = YouTube(windows.l1.text())
            windows.t.show()
            windows.waiting.show()
            windows.t.setText("0 MB/ "+str(round(yt.streams.get_by_resolution("720p").filesize/1000000,1))+" MB")
            QApplication.processEvents()
            yt.register_on_progress_callback(on_progress)
            yt.register_on_complete_callback(on_complete)
            yt.streams.get_by_resolution("720p").download(output_path=windows.l4.text())
        except Exception as e:
            print(e)
            windows.w2.show()
    else:
        windows.w2.show()

app = QApplication([])
windows = loadUi("C:/Users/jhide/Documents/_PROJECTS/youtube_downloader/project.ui")

windows.t.hide()
windows.waiting.hide()
windows.complete.hide()
windows.l4.hide()
windows.b2.hide()
windows.b3.hide()
windows.w1.hide()
windows.w2.hide()
windows.show()
windows.b1.clicked.connect(search)
windows.b2.clicked.connect(location)
windows.b3.clicked.connect(download)
app.exec_()

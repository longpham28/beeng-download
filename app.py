import PySimpleGUI as sg
from models import Comic, Downloader
import threading
import os

def download(chapters, window, path):
    downloader = Downloader()
    chapters_nums = len(chapters)
    for i, chapter in enumerate(chapters):
        downloader.download(chapter, path)
        progress = int((i + 1) / chapters_nums * 100)
        window['-PROGRESS-'].UpdateBar(progress)
url = 'https://beeng.net/truyen-tranh-online/a-tu-la-tay-du-ngoai-truyen-30363'

layout = [
    [sg.Text('Beeng Url')],
    [sg.Input(key='-COMICURL-', size=(60,20)), sg.OK(key='Fetch', button_text='Fetch')],
    [sg.Text(size=(60,1), key='-COMICNAME-')],
    [sg.Text('Chapters')],
    [sg.Listbox(values=[], size=(60, 20), key='-CHAPTERLIST-', enable_events=True, select_mode='multiple'), sg.Checkbox('Select All', key='-SELECTALL-', enable_events=True)],
    [sg.Text(text='Save To'), sg.Input(os.getcwd(), key='-SAVETO-'), sg.FolderBrowse(target='-SAVETO-')],
    [sg.Text(text='Progress'), sg.ProgressBar(100, 'h', size=(35, 20), key='-PROGRESS-')],
    [sg.OK(key='Download', button_text='Download'), sg.Cancel('Exit')]
]
window = sg.Window('Beeng Downloader', layout)
comic = None
while True:
    try:
        event, values = window.read(timeout=100)
        if event in [sg.WIN_CLOSED ,'Exit']:
            break
        if event == '-SELECTALL-':
            if not values['-SELECTALL-']:
                window['-CHAPTERLIST-'].set_value([])
            elif comic is not None:
                chapters_names = [chapter.title for chapter in comic.chapters]
                window['-CHAPTERLIST-'].set_value(chapters_names)
        if event == 'Fetch':
            url = values['-COMICURL-']
            if len(url) <= 0 or 'http' not in url:
                sg.Popup('Please type in URL')
                continue
            comic = Comic(url)
            comic.set_title()
            window['-COMICNAME-'].update(comic.title)
            comic.set_chapters()
            window['-CHAPTERLIST-'].update([chapter.title for chapter in comic.chapters])
        if event == 'Download':
            if comic is None:
                sg.Popup('Please type in url and fetch')
            if len(values['-SAVETO-']) <= 0:
                sg.Popup('Please choose folder to save')
            popup_text = 'Do you wish to start downloading {}?\n'.format(comic.title)
            for chapter_name in values['-CHAPTERLIST-']:
                popup_text = popup_text + '- {}\n'.format(chapter_name)
            ok = sg.PopupYesNo(popup_text)
            if ok:
                to_download_chapters = []
                for i in window['-CHAPTERLIST-'].get_indexes():
                    to_download_chapters.append(comic.chapters[i])
                threading.Thread(target=download, args=(to_download_chapters, window, values['-SAVETO-']), daemon=True).start()
    except Exception as e:
        sg.Popup('Error occured')
        
        

window.close()

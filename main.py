import whisper
import PySimpleGUI as sg
import io
import os.path
from PIL import Image
from pyffmpeg import FFmpeg

# GUI
# TODO: Get a file Icon

model = whisper.load_model("base")

layout = [
    [sg.T("")], [sg.Text("Choose a file: "), sg.Input(key='-FILEBROWSE-', enable_events=True), sg.FileBrowse(key="-IN-", target='-FILEBROWSE-')],
    [sg.Image(key="-IMAGE-")],
    [sg.Button("Generate Subtitles", key="-GENERATE SUBTITLES-"), sg.Text(key="-LOADING-")],
    [sg.Output(key="-SUBTITLES-", size=(100,10))]
]

### Building Window
window = sg.Window("Universal Subtitle Generator", layout, size=(600,450))
    
def transcribe(filename):
    result = model.transcribe(filename, fp16=False, language="English")
    subtitles = result["text"]
    print(subtitles)

    return subtitles

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event=="Exit":
        break
    elif event == "-FILEBROWSE-":
        filename = values["-IN-"]

        if os.path.exists(filename):
            thumbnail = "thumbnail.png"

            # Convert mp4 -> png
            ff = FFmpeg()
            ff.convert(filename, thumbnail)
            
            # Resizing Image
            image = Image.open(thumbnail)
            image.thumbnail((200, 200))
            bio = io.BytesIO()
            image.save(bio, format="PNG")
            window["-IMAGE-"].update(data=bio.getvalue())

            # Deleting thumbnail from machine
            os.remove(thumbnail)
    elif event == "-GENERATE SUBTITLES-":
        filename = values["-IN-"]

        if os.path.exists(filename):
            window["-LOADING-"].update("[Transcribing, please wait...]")
            window.perform_long_operation(lambda: transcribe(filename), "-TRANSCRIPTION DONE-")
    elif event == "-TRANSCRIPTION DONE-":
        window["-LOADING-"].update("")
        window["-SUBTITLES-"].update(values[event])

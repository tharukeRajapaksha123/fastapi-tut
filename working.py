from fastapi import FastAPI
import requests
from requests.api import get
import speech_recognition as sr 
app  = FastAPI()


download_link = "https://firebasestorage.googleapis.com/v0/b/chatapp-724ab.appspot.com/o/ROCK-MC-Memories.mp3?alt=media&token=92416788-14a6-4ca2-a1d5-40972b49ad5d"
accuracy = 0
average_reading_speed = 0.0
reading_time = 0
status = ""
text_with_errors = ""
word_count = 0




#download file
def download_file(downloadurl,filename):
    req = requests.get(downloadurl)
    with open(filename+".wav","wb") as f:
        for chunk in req.iter_content(chunk_size=8192):
            f.write(chunk)

#speech to text
def speechToText(filename):
    r =sr.Recognizer() 
    with sr.AudioFile(filename) as source:
        r.adjust_for_ambient_noise(source)

        audio = r.record(source)

        try:
            speech = r.recognize_google(audio)
            return speech
        except Exception as e:
            speech = "Error"
            return speech
    

#compare 
def compare_two_texts(textFromAudio,textFromApi):
    correct_words = 0
    textFromApiArray = textFromApi.split(" ")
    textFromAudioArray = textFromAudio.split(" ")

    # print(textFromApiArray)
    # print(textFromAudioArray)

    global word_count
    word_count = len(textFromApiArray)

    for word1 in textFromAudioArray:
        for word2 in textFromApiArray:
            if word1 == word2:
                correct_words +=1      
    return correct_words


@app.get("/{words}")
def responseToCall(words:str):
    global accuracy
    text = speechToText("download.wav")
    accuracy = compare_two_texts(text,words)
    sampleresponse = {
        "accuracy" : accuracy,
        "average_reading_speed" : average_reading_speed,
        "download_url" : download_link,
        "reading_time" : reading_time, 
        "status" : "", #success or error
        "text_with_errors" : text_with_errors,
        "word_count" : word_count
    }
    return sampleresponse


import wikipedia
import wolframalpha
import nltk
import pymysql.cursors
from nltk.tokenize import  word_tokenize
import speech_recognition as sr
import win32com.client
import sys
 
connection = pymysql.connect(host='db4free.net',
                             user='infant',
                             password='0d96ae84',
                             db='infantdb',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

if(connection):
    with connection.cursor() as cursor:
        sql = "SELECT * from dishes;"
        cursor.execute(sql)
        result = cursor.fetchall()
connection.close()

app_id = "8JJ5TK-TWVL74G25W"
client = wolframalpha.Client(app_id)

def recognize_speech_from_mic(recognizer, microphone):
    # check that recognizer and microphone arguments are appropriate type
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")
    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")
    recognizer.dynamic_energy_threshold = True
    recognizer.dynamic_energy_adjustment_damping = 0.15
    recognizer.dynamic_energy_adjustment_ratio = 1.5
    # adjust the recognizer sensitivity to ambient noise and record audio
    # from the microphone
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        
    # set up the response object
    # try recognizing the speech in the recording
     # if a RequestError or UnknownValueError exception is caught,
    #     update the response object according
        response = {"transcription":None}

 # try recognizing the speech in the recording
     # if a RequestError or UnknownValueError exception is caught,
    #update the response object accordingly
        response["transcription"] = recognizer.recognize_google(audio)

    return response

recognizer = sr.Recognizer()
microphone = sr.Microphone()
        
speaker = win32com.client.Dispatch("SAPI.SpVoice")


while True:
    print("your key pls...")
    try:
        speaker = win32com.client.Dispatch("SAPI.SpVoice")
        recognizer = sr.Recognizer()
        microphone = sr.Microphone()     
        preinp =recognize_speech_from_mic(recognizer, microphone)
        print("You said: {}".format(preinp["transcription"]))
        my_input=(preinp["transcription"])
    except sr.UnknownValueError:
        print("sry I can't get you")
        speaker.speak("sry I can't get you")
        continue
    key=["123"]
    skey=["shutdown"]
    k2=["cancel"]
    if(my_input==key[0]):
        print("you are recognized")
        speaker.speak("you are recognized")
        while True:
         print("1.normal mode\n2.computation mode\n3.information mode\n4.shut down")
         recognizer = sr.Recognizer()
         microphone = sr.Microphone()
         inp=recognize_speech_from_mic(recognizer, microphone)
         print("your Query:{}".format(inp["transcription"]))
         inp1=(inp["transcription"])
         if(inp1=="normal mode"):
             print("Logged On")
             speaker.speak("Logged On to normal mode")
             while(True):
                 try:
                     print("ask me anything")
                     speaker.speak("ask me anything")
                     que=recognize_speech_from_mic(recognizer, microphone)
                     print("your Query:{}".format(que["transcription"]))
                     que1=(que["transcription"])
                     if(que1!=k2[0]):
                          tok=word_tokenize(que1)
                          for i in range(len(tok)):
                               if(tok[i]=='dishes'):
                                    for i in range(0,len(result)):
                                         out=result[i]
                                         put1=out['dish_name']
                                         print(put1)
                                         speaker.Speak(put1)
                               if(tok[i]=='noodles'):
                                    out=result[0]
                                    put2=out['steps']
                                    print(put2)
                                    speaker.Speak(put2)
                               if(tok[i]=='toast'):
                                    out=result[1]
                                    put2=out['steps']
                                    print(put2)
                                    speaker.Speak(put2)
                               if((tok[i]=='hi')or(tok[i]=='hello')or(tok[i]=='good morning')):
                                    print("hello, good day to you")
                                    speaker.Speak("hello, good day to you")
                     else:
                         print("logged out of normal mode")
                         speaker.Speak("logged out of normal mode")
                         break
                 except(sr.UnknownValueError):
                    print("sorry i can't get you")
                    speaker.Speak("sorry i can't get you")
                    continue
                
         if(inp1=="computation mode"):
             print("Logged On")
             speaker.speak("Logged On tocomputation mode")
             while(True):
                 try:
                     try:
                         print("ask me anything")
                         speaker.speak("ask me anything")
                         inp2=recognize_speech_from_mic(recognizer, microphone)
                         print("Your Query: {}".format(inp2["transcription"]))
                         inp21=(inp2["transcription"])
                         if(inp21!=k2[0]):
                             res = client.query(inp21)
                             answer = next(res.results).text
                             print(answer)
                             speaker.Speak(answer)
                         else:
                             print("logged out of computation mode")
                             speaker.Speak("logged out of computation mode")
                             break
                     except Exception as e :
                        print("No response")
                        speaker.Speak("no response")    
                 except sr.UnknownValueError:
                    print("sry I can't get you")
                    speaker.speak("sry I can't get you")
                    continue   
                
         if(inp1=="information mode"):
             print("Logged On")
             speaker.speak("Logged On to information mode")
             while(True):
                 try:
                     try:
                         print("ask me anything")
                         speaker.speak("ask me anything")
                         inp2=recognize_speech_from_mic(recognizer, microphone)
                         print("Your Query: {}".format(inp2["transcription"]))
                         inp21=(inp2["transcription"])
                         if(inp21!=k2[0]):
                             a=wikipedia.summary(inp21,2)
                             print(a)
                             speaker.Speak(a)
                         else:
                             print("logged out of information mode")
                             speaker.Speak("logged out of information mode")
                             break
                     except Exception as e :
                         print("No response")
                         speaker.Speak("no response")
                 except sr.UnknownValueError:
                     print("sry I can't get you")
                     speaker.speak("sry I can't get you")
                     continue
    if(my_input==skey[0]):
        print("Exited")
        sys.exit()
    else:
        print("you are not he recognized person to access me...")
        sys.exit()


            

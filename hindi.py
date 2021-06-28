from flask import Flask,render_template,request,send_file
from textblob import TextBlob
from gtts import gTTS
import easyocr
import os
import cv2
#import pytesseract
from werkzeug.datastructures import FileStorage
import easyocr

#pytesseract.pytesseract.tesseract_cmd = 'C:\Program Files\Tesseract-OCR\\tesseract.exe'
UPLOAD_FOLDER = '/content'
app=Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH']= 1024 * 1024
@app.route('/',methods=['POST','GET'])
def main_page():
    if(request.method=='POST'):
        if not all(i in request.files for i in ['file']):
            return jsonify(error = 'Incorrect payload!')    
        f=request.form
        print(f)
        allow=['.png','.jpg','.tiff','.jpeg']
        image = request.files["file"]
        im='./content/input'+str(image.filename[image.filename.find('.'):])
        ext=image.filename[image.filename.find('.'):]
        print(im)
        image.save(im)
        if(ext in allow):
            if 'text' in f:
                reader = easyocr.Reader(['hi','en']) # need to run only once to load model into memory
                result = reader.readtext(im)
                s=""
                for i in result:
                    s+=i[1]+""
                return(s)
            if 'speech' in f:
                reader = easyocr.Reader(['hi','en']) # need to run only once to load model into memory
                result = reader.readtext(im)
                s=""
                for i in result:
                  s+=i[1]+"  "
                language="hi"
                output=gTTS(text=s,lang=language,slow=False)
                output.save("output1.mp3")
                os.system("start output1.mp3")
                #Audio('output1.mp3', autoplay=True)
                return(s)      
            if 'trans' in f:
                reader = easyocr.Reader(['hi','en']) # need to run only once to load model into memory
                result = reader.readtext(im)
                s=""
                for i in result:
                    s+=i[1]+"  "
                blob = TextBlob(s)
                language=request.form['lang']
                print(language)
                res=str(blob.translate(to=language))
                output=gTTS(text=res,lang=language,slow=False)
                output.save("output2.mp3")
                os.system("start output2.mp3")
                return(res)
            if 'doc' in f:
                reader = easyocr.Reader(['hi','en']) # need to run only once to load model into memory
                result = reader.readtext(im)
                s=""
                for i in result:
                    s+=i[1]+""
                file=open("text.txt","a")
                file.write(s)
                file.close
                path="text.txt"
                return send_file(path, as_attachment=True)
        else:
            return(render_template('error.html'))
    return(render_template('Project.html'))
global s
if __name__=="__main__":
  app.run(debug=True)

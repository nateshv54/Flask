import os,cv2
from flask import Flask,render_template,request,send_from_directory
from werkzeug.utils import secure_filename

UPLOAD_FOLDER='static/uploads'
ALLOWED_EXTENSIONS=set(['png','jpg','jpeg'])

#definining the flask app
app=Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT']=0
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER
app.secret_key="secret key"

if 'static' not in os.listdir('.'):
    os.mkdir('static')

if 'uploads' not in os.listdir('static/'):
    os.mkdir('static/uploads')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS

def make_sketch(img):
    grayed=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    inverted=cv2.bitwise_not(grayed)
    blurred=cv2.GaussianBlur(inverted,(19,19), sigmaX=0, sigmaY=0)
    final_result=cv2.divide(grayed,255-blurred,scale=256)
    return final_result


@app.route("/")
def home():
    return render_template("home.html")

@app.route('/sketch',methods=['POST'])
def sketch():
    file=request.files['file1']
    if file and allowed_file(file.filename):
        filename=secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
        img=cv2.imread(UPLOAD_FOLDER+'/'+filename)
        sketch_img=make_sketch(img)
        sketch_img_name=filename.split('.')[0]+'_sketch.jpg'
        _=cv2.imwrite(UPLOAD_FOLDER+'/'+sketch_img_name,sketch_img)
        return render_template('home.html',org_img_name=filename,sketch_img_name=sketch_img_name)

@app.route('/download/<filename>', methods=['GET'])
def download(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)


if __name__=="__main__":
    app.run(debug=True)

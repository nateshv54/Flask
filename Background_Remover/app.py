from rembg import remove
from PIL import Image
from werkzeug.utils import secure_filename
from flask import Flask,request,render_template
from flask import send_from_directory
import os

UPLOAD_FOLDER='static/uploads'
ALLOWED_EXTENSIONS=set(['png','jpg','jpeg','webp'])

#check if static folder exist or not
if 'static' not in os.listdir('.'):
    os.mkdir('static')

#chekc if uploads folder exists inside static or not
if 'uploads' not in os.listdir('static/'):
    os.mkdir('static/uploads')

#declaring flask app
app=Flask(__name__)

#setting few default setting using app.config
app.config['SEND_FILE_MAX_AGE_DEFAULT']=0
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER
app.secret_key="secret key"

#check the input file is in allowed extensions or not
def allowed_file(filename):
    return "." in filename and filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS

#setting paths for images storing(Local System)
def remove_background(input_path,output_path):
    input=Image.open(input_path)
    output=remove(input)
    output.save(output_path)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/removebg',methods=['POST'])
def removebg():
    print(request.files.keys())
    file=request.files['files']
    if file and allowed_file(file.filename):
        filename=secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
        rembg_img_name=filename.split('.')[0]+"rembg.png"
        remove_background(UPLOAD_FOLDER+'/'+filename,UPLOAD_FOLDER+'/'+rembg_img_name)
        return render_template('home.html',org_img_name=filename,rembg_img_name=rembg_img_name)

#downloading the image with white background
@app.route('/download/<filename>')
def download(filename):
    img_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    img = Image.open(img_path)
    img_with_bg = Image.new("RGB", img.size, (255, 255, 255))
    img_with_bg.paste(img, mask=img.split()[3])
    img_with_bg_path = os.path.join(app.config['UPLOAD_FOLDER'], 'white_' + filename)
    img_with_bg.save(img_with_bg_path)
    return send_from_directory(app.config['UPLOAD_FOLDER'], 'white_' + filename, as_attachment=True)

if __name__=="__main__":
    app.run(debug=True)

from flask import Flask,url_for,render_template,request,session
from flask_mysqldb import MySQL
from flask import redirect
from flask_mail import Mail,Message
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer

app=Flask(__name__)
app.secret_key='12345678'

app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='user1'
app.config['MYSQL_PASSWORD']='root'
app.config['MYSQL_DB']='User1'
app.config['MYSQL_CURSORCLASS']='DictCursor'

mysql = MySQL(app)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT']=587
app.config['MAIL_USE_TLS']=True
app.config['MAIL_USERNAME']='venkatv56v@gmail.com'
app.config['MAIL_PASSWORD']='ihiu jbvb bfih mqxl'
app.config['MAIL_DEFAULT_SENDER'] = 'venkatv56v@gmail.com'

mail=Mail(app)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['email']
        password = request.form['pass1']
        fname=request.form['fname']
        lname=request.form['lname']
        
        cur = mysql.connection.cursor()
        
        # Check if the username (email) already exists in the table
        result = cur.execute("SELECT * FROM user_details WHERE username = %s", (username,))

        if result > 0:
            return redirect(url_for('login1'))  # Redirect to the login page
            
        # If the username doesn't exist, insert the new user into the table
        cur.execute("INSERT INTO user_details (username, password,firstname,lastname) VALUES (%s, %s,%s,%s)", (username, password,fname,lname))
        mysql.connection.commit()
        cur.close()

        # Generate token for email verification
        serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        token = serializer.dumps(username, salt='email-confirmation')

        # Send email confirmation link
        confirm_url = url_for('confirm_email', token=token, _external=True)
        message = f"Click this link to confirm your email: {confirm_url}"
        msg = Message('Confirm your Email', recipients=[username])
        msg.body = message
        mail.send(msg)

        return 'Please check your email to confirm your registration'

    return render_template('register.html')

@app.route('/confirm_email/<token>')
def confirm_email(token):
    serializer=URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        email=serializer.loads(token,salt='email-confirmation',max_age=3600)
        return 'Email Verified Succesfully'
    except:
        return 'Invalid or expired token'

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cur = mysql.connection.cursor()
        result = cur.execute("SELECT * FROM User_details WHERE username = %s AND password = %s", (username, password))
        if result > 0:
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            return 'Incorrect username/password'
        cur.close()
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'logged_in' in session:
        username = session['username']
        return f'Logged in as {username} | <a href="/logout">Logout</a>'
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/forgot_password', methods=['GET', 'POST'])
def forget_password():
    if request.method == 'POST':
        email = request.form['username']
        # Generate token for password reset
        serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        token = serializer.dumps(email, salt='password-reset')

        # Send password reset link
        reset_url = url_for('reset_password', token=token, _external=True)
        message = f"Click this link to reset your password: {reset_url}"
        msg = Message('Reset Your Password', recipients=[email])
        msg.body = message
        mail.send(msg)

    return render_template('forgot_password.html')





@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if request.method == 'GET':
        return render_template('reset_password.html', token=token)
    
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        email = serializer.loads(token, salt='password-reset', max_age=3600)
        new_password = request.form['new_password']

        cur = mysql.connection.cursor()
        cur.execute("SELECT password FROM USER_DETAILS WHERE username=%s", (email,))
        result = cur.fetchone()
        if result != new_password:
            # Old password doesn't matches, update the password
            cur.execute("UPDATE USER_DETAILS SET password=%s WHERE username=%s", (new_password, email))
            mysql.connection.commit()
            cur.close()
            return 'Password reset successful'
        else:
            return 'Your remebers the old password. <p> Do you want to <a href="/">login</a> </p> or <a href="reset_password">reset password</a> '
    except SignatureExpired:
        return 'The password reset link has expired. Please request a new one.'
    except BadSignature:
        return 'Invalid password reset link.'
    except ValueError as e:
        return str(e)  # Return the specific error message

    

if __name__ == '__main__':
    app.run(debug=True)
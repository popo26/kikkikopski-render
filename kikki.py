from flask import Flask, render_template, redirect, url_for, request, flash
from forms import ContactForm
import boto3
import os
from dotenv import load_dotenv
import smtplib

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

SECRET_KEY = os.getenv("SECRET_KEY")
HTTPS_REDIRECT = True if os.environ.get('HTTPS_REDIRECT') else False
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
ACL = 'public-read'
S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME')
S3_REGION = os.getenv('S3_REGION') 
S3_BUCKET_PATH = os.getenv('S3_BUCKET_PATH')
MAIL_EMAIL=os.getenv('MAIL_EMAIL')
MAIL_PASSWORD=os.getenv('MAIL_PASSWORD')

if HTTPS_REDIRECT == True:
    from flask_talisman import Talisman
    Talisman(app, content_security_policy=None )

@app.route('/download/<resource>')
def download_image(resource):
    """ resource: name of the file to download"""
    s3 = boto3.client('s3',
                      aws_access_key_id=AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

    url = s3.generate_presigned_url('get_object', Params = {'Bucket': S3_BUCKET_NAME, 'Key': resource}, ExpiresIn = 100)
    return redirect(url, code=302)

@app.route("/", methods=['GET', 'POST'])
def index():
    form = ContactForm()
    if request.method=='GET':
        
        return render_template('index.html', form=form)
    
    if request.method == "POST":
        if form.validate_on_submit():
            name = request.form["name"]
            email = request.form['email']
            message = request.form['message']

            with smtplib.SMTP("smtp.gmail.com") as connection:
                connection.starttls()
                connection.login(MAIL_EMAIL, MAIL_PASSWORD)
                connection.sendmail(
                    from_addr= email, 
                    to_addrs=MAIL_EMAIL, 
                    msg=f"Subject:Received a message from Kikki Kopski site\n\n{message}\nFrom: {name}\n{email}")
               
              
            flash("Successfully submitted!")
            return redirect(url_for('index', _anchor='contact'))
        else:
            flash('Name, Email, Message are all required field.')
            return redirect(url_for('index', _anchor='contact'))

    return render_template('index.html', form=form)
    

# @app.route("/pieces")
# def pieces():
#     return render_template("work.html")



if __name__ == "__main__":
    app.run(debug=True)

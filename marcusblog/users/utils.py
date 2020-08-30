import os
import secrets
from PIL import Image
from flask import url_for
from flask_mail import Message
from marcusblog import mail
from flask import current_app



def save_picture(from_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(from_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)
    from_picture.save(picture_path)

    output_size = (125, 125)
    rs = Image.open(from_picture)
    rs.thumbnail(output_size)
    rs.save(picture_path)

    return picture_fn



    
def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='noreplay@marcusgaming.com', recipients=[user.email])
    msg.body = f'''To Reset Your Password Please Click The Following Link:{url_for('users.reset_token', token=token, _external=True)} 
If you did not make the request please ingore this mail, No changes will be made. Thanks!
Please dont reply to this mail it's an automatic generated mail.
'''
    mail.send(msg)
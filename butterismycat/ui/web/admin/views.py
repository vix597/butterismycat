'''
Admin view
'''

import os
from flask import render_template, Blueprint, g, request, url_for, redirect, flash
from werkzeug.utils import secure_filename

BLUEPRINT = Blueprint('admin', __name__)

def allowed_file(filename):
    '''
    Check if the filename is allowed by extension
    '''
    return '.' in filename and filename.rsplit('.', 1)[1] in g.allowed_extensions

@BLUEPRINT.route('/upload', methods=["GET", "POST"])
def upload():
    '''
    Load upload.html or upload file
    '''

    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(g.upload_folder, filename))
            return redirect(url_for("upload", status="success"))

    return render_template("/admin/admin.html", status=request.args.get("status", None))


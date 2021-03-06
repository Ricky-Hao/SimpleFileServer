import os
import shutil
from urllib.parse import quote
from flask import Flask, render_template, url_for, send_from_directory, redirect, request
from .setting import root_path
from .entry import Scaner

app = Flask(__name__)


@app.route('/files/')
def index():
    return render_template('index.html', path='/', entries=Scaner(root_path).entries)


@app.route('/files/<path:path>')
def show(path):
    real_path = os.path.join(root_path, path)
    parent_path = os.path.relpath(os.path.dirname(real_path), root_path)
    if not os.path.exists(real_path):
        return redirect(url_for('index'))

    if os.path.isdir(real_path):
        return render_template('index.html', parent_path=parent_path, path=path, entries=Scaner(real_path).entries)
    else:
        filename = os.path.basename(real_path)
        dirname = os.path.dirname(real_path)
        return send_from_directory(dirname, filename, as_attachment=True, attachment_filename=quote(filename))


@app.route('/files/delete', methods=['POST'])
def delete():
    path = request.get_json().get('path')
    if path is None:
        return redirect(url_for('index'))
    path = os.path.join(root_path, path)
    parent_path = os.path.relpath(os.path.dirname(path), root_path)
    if not os.path.exists(path):
        return redirect(url_for('index'))
    if os.path.isdir(path):
        shutil.rmtree(path)
    else:
        os.remove(path)
    return redirect(url_for('show', path=parent_path))


from flask import Flask
from flask import render_template, g, redirect, url_for
from flask import request

import os

from db import NoteDatabase

app = Flask(__name__)

@app.route('/')
def index():
    return redirect(url_for('text'), code=302)

@app.route('/text/', defaults={'path': ''})
@app.route('/text/<path:path>')
def text(path):
    print 'path', path
    info = app.config.db.info(path)
    documents = []
    content = ''
    notes = []
    if info['dir']:
        documents = app.config.db.list(path)
    else:
        documents = app.config.db.list(os.path.join(path, '..'))
        content = app.config.db.getContent(path)
        notes = app.config.db.listNotes(path)

    print 'notes', notes

    return render_template('text.html',
        content=content,
        notes=notes,
        path=path,
        info=info,
        title=info.get('title', '?'),
        documents=documents)


@app.route('/notes', methods=['POST'])
def notes():
    path = request.values['path']
    if 'note_id' in request.values:
        # update
        note_id = request.values['note_id']
        app.config.db.updateNote()
    else:
        # add
        start = request.values['start']
        end = request.values['end']
        text = request.values['text']
        if text:
            app.config.db.addNote(path, start, end, text)
    return redirect(url_for('text', path=path), code=302)


if __name__ == '__main__':
    import sys
    src_dir = sys.argv[1]
    app.config.db = NoteDatabase(src_dir)
    app.debug = True
    app.run()

from flask import Flask
from flask import render_template, g, redirect, url_for

from db import NoteDatabase

app = Flask(__name__)

@app.route('/')
def index():
    return redirect(url_for('notes'))

@app.route('/notes/', defaults={'path': ''})
@app.route('/notes/<path:path>')
def notes(path):
    print 'path', path
    documents = app.config.db.list(path)
    info = app.config.db.info(path)

    return render_template('notes.html',
        path=path,
        info=info,
        title=info.get('title', '?'),
        documents=documents)


if __name__ == '__main__':
    import sys
    src_dir = sys.argv[1]
    app.config.db = NoteDatabase(src_dir)
    app.debug = True
    app.run()

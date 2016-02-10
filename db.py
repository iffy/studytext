import yaml
import os
import re
from uuid import uuid4
from datetime import datetime

class NoteDatabase(object):
 
    notes_path = '_notes'

    def __init__(self, root):
        self.root = os.path.abspath(root)


    def safePath(self, childs):
        p = os.path.abspath(os.path.join(self.root, childs))
        if os.path.commonprefix([p, self.root]) != self.root:
            raise Exception("Invalid path")
        return p


    def list(self, path=''):
        """
        List the documents and folders at this path.
        """
        p = self.safePath(path)
        if not os.path.isdir(p):
            return None
        return [self.info(os.path.join(p, x)) \
            for x in os.listdir(p) if not(x.startswith('_'))]

    def info(self, path):
        """
        Get info about a particular path.
        """
        p = self.safePath(path)
        info = {
            'path': os.path.relpath(p, self.root),
            'dir': os.path.isdir(p),
            'file': os.path.isfile(p),
        }
        info['parent'] = os.path.join(info['path'], '..')
        info['name'] = os.path.basename(p)
        if info['dir']:
            # directory
            meta_filename = os.path.join(p, '_meta.yml')
            if os.path.exists(meta_filename):
                metadata = yaml.safe_load(open(meta_filename, 'rb'))
                if metadata:
                    info.update(metadata)
        else:
            # file
            if p.endswith('.md'):
                try:
                    metadata = yaml.safe_load_all(open(p, 'rb')).next()
                except StopIteration:
                    metadata = {}
                if metadata and isinstance(metadata, dict):
                    info.update(metadata)
        return info


    def getContent(self, path):
        """
        Get the content of a file.
        """
        p = self.safePath(path)
        content = open(p, 'rb').read()
        if content.startswith('---'):
            return content[content.index('---', 1)+3:].strip()
        return content

    def _noteDir(self, path, collection):
        p = self.safePath(path)
        relpart = os.path.relpath(p, self.root)
        return os.path.join(self.root, '_notes', collection, relpart)

    def addNote(self, path, start, end, text, collection='default'):
        """
        Add a note for the text in a file.
        """
        note_file = os.path.join(self._noteDir(path, collection), 'notes.yml')
        dirname = os.path.dirname(note_file)
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        current = []
        if os.path.exists(note_file):
            current = yaml.safe_load(open(note_file, 'rb').read())
        current.append({
            'id': str(uuid4()),
            'date': datetime.now().isoformat(),
            'start': start,
            'end': end,
            'text': text,
        })
        with open(note_file, 'wb') as fh:
            fh.write(yaml.safe_dump(current, default_flow_style=False))
        return current[-1]

    def listNotes(self, path, collection='default'):
        """
        List notes for a file.
        """
        note_file = os.path.join(self._noteDir(path, collection), 'notes.yml')
        if os.path.exists(note_file):
            return yaml.safe_load(open(note_file, 'rb').read())
        else:
            return []

    def updateNote(self, path, note_id, text, collection='default'):
        """
        Update an existing note.
        """
        raise NotImplementedError("Not implemented yet")




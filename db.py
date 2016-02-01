import yaml
import os

class NoteDatabase(object):
    
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
        if info['dir']:
            meta_filename = os.path.join(p, '_meta.yml')
            if os.path.exists(meta_filename):
                metadata = yaml.safe_load(open(meta_filename, 'rb'))
                if metadata:
                    info.update(metadata)
        return info




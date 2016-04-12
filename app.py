#!/usr/bin/python2

from flask import Flask, request, render_template, jsonify
import os


class Config(object):
    DEBUG = True
    NOTES_FILE = './notes.txt'


class NotesFile(object):
    def __init__(self, name):
        self.name = name
        if not os.path.exists(name):
            f = open(name, 'w')
            f.close()

    def get_all(self):
        f = open(self.name, 'r')
        lines = [x.split(';') for x in filter(None, f.read().split('\n'))]
        f.close()

        print lines

        return [
            {'id': int(line[0]), 'title': line[1], 'content': line[2]}
            for line
            in lines
        ]

    def save_all(self, notes):
        f = open(self.name, 'w')
        print notes
        f.write('\n'.join([
            ';'.join([str(note['id']), note['title'], note['content']])
            for note
            in notes
        ]) + '\n')
        f.close()

    def add_note(self, title, content):
        notes = self.get_all()

        ids = [note['id'] for note in notes]

        if len(ids):
            max_id = max(ids)
        else:
            max_id = 0

        f = open(self.name, 'a+')
        f.write(u'{};{};{}\n'.format(max_id + 1, title, content))
        f.close()

    def delete_note(self, id):
        notes = self.get_all()

        notes = filter(lambda note: note['id'] != int(id), notes)

        self.save_all(notes)


app = Flask(__name__)
app.config.from_object(Config)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/list_notes')
def list_notes():
    notes_file = NotesFile(Config.NOTES_FILE)
    return jsonify(dict(result=notes_file.get_all()))


@app.route('/api/add_note')
def add_note():
    title = request.args['title']
    content = request.args['content']

    notes_file = NotesFile(Config.NOTES_FILE)
    notes_file.add_note(title=title, content=content)
    return jsonify(dict(result=notes_file.get_all()))


@app.route('/api/delete_note')
def delete_note():
    id = request.args['id']

    notes_file = NotesFile(Config.NOTES_FILE)
    notes_file.delete_note(id=id)
    return jsonify(dict(result=notes_file.get_all()))


app.run(host='0.0.0.0', port=8000, threaded=True)

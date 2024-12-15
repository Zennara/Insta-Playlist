import json

# create notes.json if it does not exist
try:
    with open("notes.json", "r") as f:
        pass
except FileNotFoundError:
    with open("notes.json", "w") as f:
        json.dump([], f)


def add_note(note_id: str):
    notes = get_notes()
    notes.append(note_id)
    with open("notes.json", "w") as f:
        json.dump(notes, f)


def get_notes():
    with open("notes.json", "r") as f:
        return json.load(f)


def is_note_added(note_id: str):
    for previous_note in get_notes():
        if previous_note == note_id:
            return True

from datetime import datetime
from flask import request
from flask_smorest import Blueprint, abort
from flask.views import MethodView
from marshmallow import Schema, fields, validate, ValidationError

# PUBLIC_INTERFACE
class NoteSchema(Schema):
    """Schema for a Note object used in API responses."""
    id = fields.Int(dump_only=True, description="Unique identifier for the note")
    title = fields.Str(required=True, validate=validate.Length(min=1, max=255), description="Title of the note")
    content = fields.Str(required=True, validate=validate.Length(min=1), description="Body content of the note")
    created_at = fields.DateTime(dump_only=True, description="Creation timestamp in ISO8601")
    updated_at = fields.DateTime(dump_only=True, description="Last update timestamp in ISO8601")


# PUBLIC_INTERFACE
class NoteCreateSchema(Schema):
    """Schema for creating a note."""
    title = fields.Str(required=True, validate=validate.Length(min=1, max=255), description="Title of the note")
    content = fields.Str(required=True, validate=validate.Length(min=1), description="Body content of the note")


# PUBLIC_INTERFACE
class NoteUpdateSchema(Schema):
    """Schema for updating a note."""
    title = fields.Str(required=False, validate=validate.Length(min=1, max=255), description="Title of the note")
    content = fields.Str(required=False, validate=validate.Length(min=1), description="Body content of the note")


blp = Blueprint(
    "Notes",
    "notes",
    url_prefix="/notes",
    description="CRUD operations for notes"
)

# Simple adaptive storage: in-memory fallback; placeholder hooks for DB autodetect
# In a real setup, you could check for SQLALCHEMY_DATABASE_URI or related env vars.
_use_memory = True
_notes_store = {}
_next_id = 1


def _now_iso():
    return datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


def _validate_json(schema_cls):
    try:
        payload = request.get_json()
        if payload is None:
            abort(400, message="Invalid or missing JSON body")
        data = schema_cls().load(payload)
        return data
    except ValidationError as err:
        abort(400, message="Validation error", errors=err.messages)


@blp.route("/", methods=["GET"])
class NotesList(MethodView):
    """List and create notes."""
    # PUBLIC_INTERFACE
    def get(self):
        """Return a list of all notes.
        Returns:
            200 JSON array of notes.
        """
        items = list(_notes_store.values())
        return {"items": items, "count": len(items)}, 200

    # PUBLIC_INTERFACE
    def post(self):
        """Create a new note.
        Body:
            NoteCreateSchema JSON.
        Returns:
            201 Created with the new note.
        """
        global _next_id
        data = _validate_json(NoteCreateSchema)

        note_id = _next_id
        _next_id += 1
        now = _now_iso()
        note = {
            "id": note_id,
            "title": data["title"],
            "content": data["content"],
            "created_at": now,
            "updated_at": now,
        }
        _notes_store[note_id] = note
        return note, 201


@blp.route("/<int:note_id>", methods=["GET", "PUT", "DELETE"])
class NoteDetail(MethodView):
    """Retrieve, update, and delete a single note by id."""
    # PUBLIC_INTERFACE
    def get(self, note_id: int):
        """Get a note by id.
        Params:
            note_id path param.
        Returns:
            200 with note, or 404 if not found.
        """
        note = _notes_store.get(note_id)
        if not note:
            abort(404, message="Note not found")
        return note, 200

    # PUBLIC_INTERFACE
    def put(self, note_id: int):
        """Update a note by id.
        Body:
            NoteUpdateSchema JSON. At least one field required.
        Returns:
            200 with updated note or 404 if not found.
        """
        note = _notes_store.get(note_id)
        if not note:
            abort(404, message="Note not found")

        data = _validate_json(NoteUpdateSchema)
        if not data:
            abort(400, message="No valid fields provided")

        updated = False
        if "title" in data:
            note["title"] = data["title"]
            updated = True
        if "content" in data:
            note["content"] = data["content"]
            updated = True
        if updated:
            note["updated_at"] = _now_iso()
        return note, 200

    # PUBLIC_INTERFACE
    def delete(self, note_id: int):
        """Delete a note by id.
        Returns:
            204 No Content on success, or 404 if not found.
        """
        if note_id not in _notes_store:
            abort(404, message="Note not found")
        _notes_store.pop(note_id, None)
        return "", 204

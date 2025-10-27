# Notes Backend (Flask)

This service exposes a simple Notes REST API with in-memory storage by default. It includes OpenAPI docs via flask-smorest and CORS enabled for all origins.

Run:
- The preview system runs the app on port 3001.
- Docs are available at /docs and the generated OpenAPI at /openapi.json.

Health:
- GET / -> 200 {"message":"Healthy"}

Notes Endpoints:
- GET /notes -> 200 {"items":[...], "count": N}
- POST /notes -> 201 {id, title, content, created_at, updated_at}
  Request body: {"title": "My title", "content": "My content"}
- GET /notes/<id> -> 200 {note} or 404 if not found
- PUT /notes/<id> -> 200 {updated note} or 404 if not found
  Request body: {"title": "...", "content": "..."} (either or both)
- DELETE /notes/<id> -> 204 No Content or 404 if not found

Validation:
- JSON body is required for POST/PUT with fields validated via marshmallow.
- Errors return JSON with message and optional errors details.

CORS:
- All origins allowed for simplicity.

Self-check:
- Open / to verify health.
- Use /docs for interactive API documentation.
- Create a note: curl -X POST http://localhost:3001/notes -H "Content-Type: application/json" -d '{"title":"t","content":"c"}'
- List notes: curl http://localhost:3001/notes
- Update note: curl -X PUT http://localhost:3001/notes/1 -H "Content-Type: application/json" -d '{"title":"T2"}'
- Delete note: curl -X DELETE http://localhost:3001/notes/1

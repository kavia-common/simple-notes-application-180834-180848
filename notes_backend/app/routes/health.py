from flask_smorest import Blueprint
from flask.views import MethodView

# Health check blueprint, exposed at the root path
blp = Blueprint("Health", "health", url_prefix="/", description="Health check route")


@blp.route("/")
class HealthCheck(MethodView):
    # PUBLIC_INTERFACE
    def get(self):
        """Return a simple health payload."""
        return {"message": "Healthy"}, 200

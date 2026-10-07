from app.main import app


def test_app_boots_and_has_health_route():
    routes = {getattr(route, "path", None) for route in app.routes}
    assert "/health" in routes

from app import app


def test_home_page():

    tester = app.test_client()

    response = tester.get("/")

    assert response.status_code == 200


def test_threats_page():

    tester = app.test_client()

    response = tester.get("/threats")

    assert response.status_code == 200


def test_compare_page():

    tester = app.test_client()

    response = tester.get("/compare")

    assert response.status_code == 200


def test_about_page():

    tester = app.test_client()

    response = tester.get("/about")

    assert response.status_code == 200


def test_404_page():

    tester = app.test_client()

    response = tester.get("/randompage")

    assert response.status_code == 404
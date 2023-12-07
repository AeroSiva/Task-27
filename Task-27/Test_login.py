import pytest
from main import Login


@pytest.fixture
def zen_instance():
    login_logout = Login()
    login_logout.access_url()
    yield login_logout
    login_logout.driver.quit()

def test_login(zen_instance):
    zen_instance.login_logout_test()
import os
import sys
import django
from django.conf import settings
from django.test.utils import get_runner, teardown_test_environment, setup_test_environment
import logging

# Setup logging
logging.basicConfig(level=logging.DEBUG)

def run_tests():
    # Add the project directory to the Python path
    sys.path.append(os. getcwd())
    os.environ['DJANGO_SETTINGS_MODULE'] = 'heron.test_settings'
    logging.debug("DJANGO_SETTINGS_MODULE set to 'heron.test_settings'")
    django.setup()
    logging.debug("Django setup complete")


    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    logging.debug(f"TestRunner instantiated: {test_runner}")

    # Run the tests
    failures = test_runner.run_tests(['vfw_home.tests'])
    logging.debug(f"Test run completed with failures: {failures}")
    if failures:
        sys.exit(bool(failures))


if __name__ == '__main__':
    run_tests()
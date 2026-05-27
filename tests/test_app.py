import unittest
import os

class TestApp(unittest.TestCase):
    
    def test_requirements_exist(self):
        self.assertTrue(os.path.exists('requirements.txt'))
    
    def test_dockerfile_exists(self):
        self.assertTrue(os.path.exists('Dockerfile'))
    
    def test_docker_compose_exists(self):
        self.assertTrue(os.path.exists('docker-compose.yml'))
    
    def test_app_exists(self):
        self.assertTrue(os.path.exists('app.py'))

if __name__ == '__main__':
    unittest.main()
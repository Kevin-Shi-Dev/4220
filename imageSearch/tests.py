from django.test import TestCase

# Create your tests here.
class ViewTestCase(TestCase):
    # Test for checking to see if we get 200 OK on homepage
    def test_home(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    # Test for checking to see if we get 200 OK on upload page
    def test_upload_page(self):
        response = self.client.get('/upload')
        self.assertEqual(response.status_code, 200)

    # Test for checking to see if 200 is returned from image page
    def test_image_page(self):
        response = self.client.get('/image')
        self.assertEqual(response.status_code, 200)
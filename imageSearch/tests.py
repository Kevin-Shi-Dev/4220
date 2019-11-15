from django.test import TestCase
from imageSearch.views import get_img_type

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

    def test_search_results_width(self):
        response = self.client.post('/search', {'search_term': '', 'width': '700', 'img_type': ''})
        self.assertEqual(response.status_code, 200)

    def test_search_results_term(self):
        response = self.client.post('/search', {'search_term': 'senko', 'width': '0', 'img_type': ''})
        self.assertEqual(response.status_code, 200)

    def test_search_results_type(self):
        response = self.client.post('/search', {'search_term': '', 'width': '0', 'img_type': 'png'})
        self.assertEqual(response.status_code, 200)

    def test_get_image_type(self):
        self.assertEqual(get_img_type('image/jpeg'), 'jpg')
        self.assertEqual(get_img_type('image/png'), 'png')
        self.assertEqual(get_img_type('image/gif'), '')

    def test_gallery_get(self):
        response = self.client.get('/gallery')
        self.assertEqual(response.status_code, 200)

    def test_gallery_post(self):
        response = self.client.post('/gallery', {'search_term': '', 'width': '0', 'img_type': ''})
        self.assertEqual(response.status_code, 200)

    def test_contact(self):
        response = self.client.get('/contact')
        self.assertEqual(response.status_code, 200)

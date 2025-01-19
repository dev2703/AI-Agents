import unittest
from social_media_agent import SocialMediaAgent

class TestSocialMediaAgent(unittest.TestCase):

    def test_post_content(self):
        agent = SocialMediaAgent()
        result = agent.post_content("Hello World!")
        self.assertTrue(result)  # Replace with actual assertion based on the result

    def test_invalid_post_content(self):
        agent = SocialMediaAgent()
        with self.assertRaises(ValueError):  # Assuming invalid input triggers a ValueError
            agent.post_content("")  # Empty content should be invalid

if __name__ == '__main__':
    unittest.main()

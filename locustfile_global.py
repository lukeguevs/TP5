from locust import task, between, TaskSet, HttpUser, User
from client import SocialMediaClient

class GlobalTaskSet(TaskSet):
    def __init__(self, user: User):
        super().__init__(user)
        self.social_media_client = SocialMediaClient(self.client)

    def on_start(self):
        self.social_media_client.login()

    @task(353)
    def view_feed_api(self):
        self.social_media_client.view_feed()

    @task(235)
    def like_post_api(self):
        self.social_media_client.like_post()

    @task(223)
    def view_profile_api(self):
        self.social_media_client.view_profile()

    @task(149)
    def follow_user_api(self):
        self.social_media_client.follow_user()

    @task(52)
    def create_post_api(self):
        self.social_media_client.create_post()

    @task(10)
    def login_api(self):
        self.social_media_client.login()

class GlobalSocialMediaUser(HttpUser):
    wait_time = between(1, 5)
    tasks = [GlobalTaskSet]

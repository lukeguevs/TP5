from locust import task, between, TaskSet, User, HttpUser
from client import SocialMediaClient
from locust.user.markov_taskset import MarkovTaskSet, transition, transitions

class MarkovTaskSet(MarkovTaskSet):
    def __init__(self, user: User):
        super().__init__(user)
        self.social_media_client = SocialMediaClient(self.client)

    def on_start(self):
        self.social_media_client.login()
    
    @transition('view_feed')
    def login(self):
        self.social_media_client.login()
    
    @transitions([('login', 1), ('like', 23), ('view_profile', 24),
                  ('post', 5), ('view_feed', 32), ('follow', 14)])
    def view_feed(self):
        self.social_media_client.view_feed()
    
    @transitions([('login', 1), ('like', 25),
                  ('follow', 16), ('view_feed', 37),
                  ('view_profile', 19), ('post', 6)])
    def like(self):
        self.social_media_client.like_post()
    
    @transitions([('login', 1), ('like', 24),
                  ('post', 5), ('view_feed', 37),
                  ('follow', 13), ('view_profile', 20)])
    def view_profile(self):
        self.social_media_client.view_profile()
    
    @transitions([('login', 1), ('view_feed', 38),
                  ('view_profile', 22), ('follow', 17),
                  ('like', 21), ('post', 1)])
    def follow(self):
        self.social_media_client.follow_user()
    
    @transitions([('view_profile', 27), ('like', 21),
                  ('follow', 21), ('view_feed', 23),
                  ('post', 8)]) 
    def post(self):
        self.social_media_client.create_post()
        
class MarkovSocialMediaUser(HttpUser):
    wait_time = between(1, 5)
    tasks = [MarkovTaskSet]
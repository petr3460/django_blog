
import pdb
from .models import UserProfile



def save_profile(backend, user, response, *args, **kwargs):
    if backend.name == 'vk-oauth2':
        avatar = response['photo']
    if backend.name == 'twitter':
        avatar = response['profile_image_url']

    if not UserProfile.objects.filter(user_id=user.id):
        UserProfile.objects.create(user_id=user.id, avatar=avatar)
    #pdb.set_trace()
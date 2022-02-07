import logging

from website.models import Photo
import cloudinary
from cloudinary import api, utils

logger = logging.getLogger(__name__)


def get_categories() -> list:
    folders = cloudinary.api.subfolders("photos")['folders']
    categories = [p['name'] for p in folders]
    return categories


def get_photos(category: str) -> list:
    pref = "photos/{}/".format(category)
    return cloudinary.api.resources(type='upload', prefix=pref, max_results=200)['resources']


def load_photos():
    categories = get_categories()
    photos_in_database = {}
    photos_in_cloudinary = {}
    for c in categories:
        photos = []
        for f in get_photos(c):
            file = f['public_id'].split('/')[-1] + '.jpg'
            photos.append(file)
            photo = Photo.objects.filter(filename=file)
            if not photo:
                filepath = "photos/{}/".format(c) + file
                if f['height'] > f['width']:
                    orientation = "p"
                    url_small = utils.cloudinary_url(filepath, height=640, crop="scale", sign_url=True)
                else:
                    orientation = "l"
                    url_small = utils.cloudinary_url(filepath, width=640, crop="scale", sign_url=True)
                photo = Photo(filename=file, url=f["secure_url"], url_small=url_small[0], category=c,
                              description="placeholder", orientation=orientation).save()
                logger.info('Added %s to database.' % file)
        photos_in_cloudinary[c] = photos
        photos_in_database[c] = list(Photo.objects.filter(category=c).order_by('filename'))
        for p in photos_in_database[c]:
            if p.filename not in photos_in_cloudinary[c]:
                logger.info('Removed %s from database.' % p.filename)
                p.delete()
                photos_in_database[c].remove(p)
    return photos_in_database

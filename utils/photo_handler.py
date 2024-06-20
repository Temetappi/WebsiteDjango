import logging

from website.models import Photo
import cloudinary
from cloudinary import api, utils

logger = logging.getLogger(__name__)


def get_photos(path: str) -> list:
    return cloudinary.api.resources(type='upload', prefix=path, max_results=200)['resources']


def load_photos():
    photos_in_cloudinary = list()
    for f in get_photos(f"photos/people/"):
        file = f['public_id'].split('/')[-1] + '.jpg'
        photos_in_cloudinary.append(file)
        photo = Photo.objects.filter(filename=file)
        if not photo:
            filepath = f"photos/people/{file}"
            if f['height'] > f['width']:
                orientation = "p"
                url_small = utils.cloudinary_url(filepath, height=640, crop="scale", sign_url=True)
            else:
                orientation = "l"
                url_small = utils.cloudinary_url(filepath, width=640, crop="scale", sign_url=True)
            Photo(filename=file, created=f["created_at"], url=f["secure_url"], url_small=url_small[0], category="people",
                          description="placeholder", orientation=orientation).save()
            logger.info('Added %s to database.' % file)
    photos_in_database = list(Photo.objects.filter(category="people").order_by('filename'))
    for p in photos_in_database:
        if p.filename not in photos_in_cloudinary:
            logger.info('Removed %s from database.' % p.filename)
            p.delete()
            photos_in_database.remove(p)
    return photos_in_database

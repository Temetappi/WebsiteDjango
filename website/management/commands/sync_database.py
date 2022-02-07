from django.core.management.base import BaseCommand
from utils.photo_handler import load_photos


class Command(BaseCommand):
    help = "Sync the database with photos from Cloudinary"

    def handle(self, *args, **kwargs):
        load_photos()
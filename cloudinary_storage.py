import os
import cloudinary
import cloudinary.uploader
import cloudinary.api
import logging

logger = logging.getLogger(__name__)

def configurer_cloudinary(app):
    cloud_name = app.config.get('CLOUDINARY_CLOUD_NAME', '')
    api_key = app.config.get('CLOUDINARY_API_KEY', '')
    api_secret = app.config.get('CLOUDINARY_API_SECRET', '')
    if cloud_name and api_key and api_secret:
        cloudinary.config(
            cloud_name=cloud_name,
            api_key=api_key,
            api_secret=api_secret,
            secure=True
        )
        return True
    return False

def uploader_image(file, dossier='locauto'):
    try:
        result = cloudinary.uploader.upload(
            file,
            folder=dossier,
            resource_type='image'
        )
        url = result.get('secure_url', '')
        public_id = result.get('public_id', '')
        logger.info(f"Image uploadée sur Cloudinary: {url}")
        return url, public_id
    except Exception as e:
        logger.error(f"Erreur upload Cloudinary: {e}")
        return None, None

def supprimer_image(public_id):
    try:
        cloudinary.uploader.destroy(public_id)
        logger.info(f"Image supprimée: {public_id}")
        return True
    except Exception as e:
        logger.error(f"Erreur suppression Cloudinary: {e}")
        return False

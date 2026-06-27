import cloudinary.uploader
from pathlib import Path
from django.conf import settings
from django.core.management.base import BaseCommand
from apps.products.models import ProductImage


class Command(BaseCommand):
    help = 'Upload local product images to Cloudinary'

    def handle(self, *args, **options):
        if not getattr(settings, 'CLOUDINARY_URL', ''):
            self.stdout.write('CLOUDINARY_URL not set — skipping')
            return

        media_root = Path(settings.BASE_DIR) / 'static' / 'media'
        uploaded = 0
        skipped = 0

        for pi in ProductImage.objects.all():
            local_path = media_root / pi.image.name
            if not local_path.exists():
                self.stdout.write(f'SKIP (no file): {pi.image.name}')
                skipped += 1
                continue

            stem   = Path(pi.image.name).stem
            folder = str(Path(pi.image.name).parent).replace('\\', '/')
            public_id = f'media/{folder}/{stem}'

            try:
                cloudinary.uploader.upload(
                    str(local_path),
                    public_id=public_id,
                    overwrite=False,
                    resource_type='image',
                )
                self.stdout.write(f'OK: {public_id}')
                uploaded += 1
            except Exception as e:
                self.stdout.write(f'ERROR {pi.image.name}: {e}')

        self.stdout.write(f'Done: {uploaded} uploaded, {skipped} skipped')

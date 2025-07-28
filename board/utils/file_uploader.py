import logging
import uuid
import os
from django.conf import settings
from django.core.files.uploadedfile import UploadedFile

logger = logging.getLogger('prod')


class FileUploader:
    @staticmethod
    def upload_file(file_data: UploadedFile, file_type: str = "general") -> str:
        if not file_data:
            return None

        original_filename = file_data.name if hasattr(
            file_data, 'name') else "unknown"
        file_extension = original_filename.split(
            '.')[-1] if '.' in original_filename else "bin"
        unique_filename = f"{uuid.uuid4().hex}.{file_extension}"

        upload_dir = os.path.join(settings.MEDIA_ROOT, file_type)
        os.makedirs(upload_dir, exist_ok=True)

        file_path = os.path.join(upload_dir, unique_filename)

        try:
            with open(file_path, 'wb+') as destination:
                for chunk in file_data.chunks():
                    destination.write(chunk)
            logger.info(
                f"FileUploader: '{original_filename}'({file_type}) 로컬 저장 완료. 경로: {file_path}")
        except Exception as e:
            logger.error(
                f"FileUploader: 파일 '{original_filename}' 로컬 저장 중 오류 발생: {e}")
            return None

        file_url = f"{settings.MEDIA_URL}{file_type}/{unique_filename}"

        return file_url

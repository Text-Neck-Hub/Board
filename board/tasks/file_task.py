import logging
import uuid

logger = logging.getLogger('prod')


class FileTask:
    pass
    # @staticmethod
    # def create_file(file_data, file_type="image"):
    #     if not file_data:
    #         return None

    #     file_extension = "jpg" if file_type == "image" else "pdf"
    #     unique_filename = f"{uuid.uuid4().hex}_{file_type}.{file_extension}"
    #     mock_cdn_url = f"https://my.mockcdn.com/{file_type}s/{unique_filename}"

    #     logger.info(
    #         f"FileUploader: {file_type} 업로드 모의 완료. URL: {mock_cdn_url}")

    #     return mock_cdn_url

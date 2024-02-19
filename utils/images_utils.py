import os

class ImagesUtils:
    @staticmethod
    def save_image_and_get_path(unique_id, frame_data):
        filename = ImagesUtils._get_image_filename(unique_id)
        ImagesUtils._save_image_locally(frame_data, filename)
        return filename

    @staticmethod
    def _get_image_filename(unique_id):
        current_dir = os.path.dirname(__file__)
        parent_dir = os.path.dirname(current_dir)
        target_folder_dir = os.path.join(parent_dir, 'assets')
        filename = os.path.join(target_folder_dir, f'rocket_{unique_id}.jpg')
        return filename
    
    @staticmethod 
    def _save_image_locally(image_bytes, filename):
        with open(filename, 'wb') as image_file:
            image_file.write(image_bytes)
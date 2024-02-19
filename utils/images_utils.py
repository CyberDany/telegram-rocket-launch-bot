import os

class ImagesUtils:
    @staticmethod
    def save_image_and_get_path(unique_id: str, frame_data: bytes):
        """
        Saves image data to disk and returns the file path.
        
        Parameters:
        - unique_id: Identifier for generating a unique file name.
        - frame_data: Byte data of the image.
        
        Returns:
        - The path to the saved image file.
        """
        filename = ImagesUtils._get_image_filename(unique_id)
        ImagesUtils._save_image_locally(frame_data, filename)
        return filename

    @staticmethod
    def _get_image_filename(unique_id: str):
        """
        Generates a file path for an image using a unique identifier.
        
        Parameters:
        - unique_id: Used for filename uniqueness.
        
        Returns:
        - Full path for saving the image.
        """
        current_dir = os.path.dirname(__file__)
        parent_dir = os.path.dirname(current_dir)
        target_folder_dir = os.path.join(parent_dir, 'assets')
        filename = os.path.join(target_folder_dir, f'rocket_{unique_id}.jpg')
        return filename
    
    @staticmethod 
    def _save_image_locally(image_bytes: bytes, filename: str):
        """
        Writes image byte data to a file.
        
        Parameters:
        - image_bytes: Raw bytes of the image.
        - filename: Path where the image will be saved.
        """
        with open(filename, 'wb') as image_file:
            image_file.write(image_bytes)
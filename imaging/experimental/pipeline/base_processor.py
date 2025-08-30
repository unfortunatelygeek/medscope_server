from abc import ABC, abstractmethod

class ImageProcessor(ABC):
    """
    Abstract base class for image processing pipelines.
    """

    @abstractmethod
    def preprocess(self, image, augment=False):
        """
        Preprocess the input image.
        :param image: Input image (can be a PIL image, numpy array, or file path).
        :param augment: Boolean flag to apply data augmentation.
        :return: Preprocessed image ready for inference.
        """
        pass

    @abstractmethod
    def run_inference(self, preprocessed_image):
        """
        Run inference on the preprocessed image.
        :param preprocessed_image: Image after preprocessing.
        :return: Raw model predictions.
        """
        pass

    @abstractmethod
    def postprocess(self, inference_results):
        """
        Postprocess raw model output to structured results.
        :param inference_results: Raw model predictions.
        :return: Dictionary of processed results.
        """
        pass

    @abstractmethod
    def process_for_training(self, image_path):
        """
        Prepare image with augmentation for training.
        :param image_path: Path to the image file.
        :return: Augmented, preprocessed image.
        """
        pass
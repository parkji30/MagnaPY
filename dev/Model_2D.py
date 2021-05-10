from Model import Model

class Model1D(Model):
    """
    Model class for 2 dimensional model structures.
    """


    def __init__(self, image_name, quantization_numbers):
        """
        """
        super(Model, self).__init__(image_name, quantization_numbers)
        self.quantization_numbers = quantization_numbers
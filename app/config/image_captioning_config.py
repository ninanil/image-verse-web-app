class ImageCaptioningConfig:
    def __init__(
        self,
        model_name: str = "ImageCaptioningModelV1",
        caption_model: str = "microsoft/Florence-2-large",
        processor: str = "microsoft/Florence-2-large",
        max_new_tokens: int = 1024,
        do_sample:bool = False ,
        num_beams: int = 3
    ):
        self.model_name = model_name
        self.caption_model = caption_model
        self.processor = processor
        self.max_new_tokens = max_new_tokens
        self.do_sample = do_sample
        self.num_beams = num_beams

class StableDiffusionConfig:
    def __init__(
        self,
        model_name: str = "StableDiffusionV2",
        num_inference_steps: int = 50,
        guidance_scale: float = 7.5,
        seed: int = 64,
        vae_model: str = "CompVis/stable-diffusion-v1-4",
        tokenizer_model: str = "openai/clip-vit-large-patch14",
        text_encoder_model: str = "openai/clip-vit-large-patch14",
        unet_model: str = "CompVis/stable-diffusion-v1-4",
        scheduler_model: str = "CompVis/stable-diffusion-v1-4"
    ):
        assert num_inference_steps > 0, "Number of inference steps must be positive"
        assert guidance_scale > 0, "Guidance scale must be positive"

        self.model_name = model_name
        self.num_inference_steps = num_inference_steps
        self.guidance_scale = guidance_scale
        self.seed = seed
        self.vae_model = vae_model
        self.tokenizer_model = tokenizer_model
        self.text_encoder_model = text_encoder_model
        self.unet_model = unet_model
        self.scheduler_model = scheduler_model

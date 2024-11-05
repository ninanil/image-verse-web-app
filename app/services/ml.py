import torch
from transformers import CLIPTextModel, CLIPTokenizer, AutoProcessor, AutoModelForCausalLM
from diffusers import AutoencoderKL, UNet2DConditionModel, PNDMScheduler
from PIL import Image
from fastapi import UploadFile
from tqdm.auto import tqdm
from app.utils.app_logger import logger


class StableDiffusionModel:
    def __init__(self,config):
        
        logger.info(
            "Initializing StableDiffusionModel with num_inference_steps=%d, guidance_scale=%f, seed=%d",
            config.num_inference_steps, config.guidance_scale, config.seed
        )
        
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.num_inference_steps = config.num_inference_steps
        self.guidance_scale = config.guidance_scale
        self.generator = torch.manual_seed(config.seed)

        logger.info("Loading models...")
        self.vae = AutoencoderKL.from_pretrained(config.vae_model, subfolder="vae").to(self.device)
        self.tokenizer = CLIPTokenizer.from_pretrained(config.tokenizer_model)
        self.text_encoder = CLIPTextModel.from_pretrained(config.text_encoder_model).to(self.device)
        self.unet = UNet2DConditionModel.from_pretrained(config.unet_model, subfolder="unet").to(self.device)
        self.scheduler = PNDMScheduler.from_pretrained(config.scheduler_model, subfolder="scheduler")


    def latents_to_pil(self, latents):
        logger.info("Converting latents to PIL images...")
        latents = (1 / 0.18215) * latents
        with torch.no_grad():
            image = self.vae.decode(latents).sample
        image = (image / 2 + 0.5).clamp(0, 1)
        image = image.detach().cpu().permute(0, 2, 3, 1).numpy()
        images = (image * 255).round().astype("uint8")
        pil_images = [Image.fromarray(image) for image in images]
        logger.info("Successfully converted latents to %d PIL images", len(pil_images))
        return pil_images

    def prompt_to_emb(self, prompt, negative_prompts=''):
        logger.info("Converting prompts to embeddings...")
        if isinstance(prompt, list):
            batch_size = len(prompt)
        else :
            batch_size = 1

        text_inputs = self.tokenizer(
            prompt,
            padding="max_length",
            max_length=77,
            truncation=True,
            return_tensors="pt",
        )
        text_input_ids = text_inputs.input_ids
        prompt_embeds = self.text_encoder(text_input_ids.to(self.device))
        prompt_embeds = prompt_embeds[0]
        prompt_embeds_dtype = self.text_encoder.dtype
        prompt_embeds = prompt_embeds.to(dtype=prompt_embeds_dtype, device=self.device)
        _, seq_len, _ = prompt_embeds.shape
        prompt_embeds = prompt_embeds.repeat(1, 1, 1).view(batch_size * 1, seq_len, -1)

        negative_text_inputs = self.tokenizer(
            negative_prompts,
            padding="max_length",
            max_length=77,
            truncation=True,
            return_tensors="pt",
        )
        negative_input_ids = negative_text_inputs.input_ids
        negative_prompt_embeds = self.text_encoder(negative_input_ids.to(self.device))[0]
        negative_prompt_embeds = negative_prompt_embeds.to(dtype=prompt_embeds_dtype, device=self.device)
        _, seq_len, _ = negative_prompt_embeds.shape
        negative_prompt_embeds = negative_prompt_embeds.repeat(1, 1, 1).view(batch_size * 1, seq_len, -1)

        concatenated_embeddings = torch.cat([negative_prompt_embeds, prompt_embeds])
        logger.info("Successfully converted prompts to embeddings")
        return concatenated_embeddings

    def emb_to_latents(self, text_embeddings):
        logger.info("Generating latents from embeddings...")
        self.scheduler.set_timesteps(self.num_inference_steps)
        latents = torch.randn((1, 4, 64, 64), dtype=torch.float32).to(self.device)

        for t in tqdm(self.scheduler.timesteps):
            logger.debug("Processing timestep %s", t)
            latent_model_input = torch.cat([latents] * 2)
            latent_model_input = self.scheduler.scale_model_input(latent_model_input, t)
            with torch.no_grad():
                noise_pred = self.unet(latent_model_input, t, encoder_hidden_states=text_embeddings, return_dict=False, added_cond_kwargs={'text_embeds': text_embeddings})[0]
            noise_pred_uncond, noise_pred_text = noise_pred.chunk(2)
            noise_pred = noise_pred_uncond + self.guidance_scale * (noise_pred_text - noise_pred_uncond)
            latents = self.scheduler.step(noise_pred, t, latents, return_dict=False)[0]

        logger.info("Successfully generated latents")
        return latents
    def generate_image(self,prompt):
        with torch.amp.autocast('cuda') if self.device == "cuda" else torch.no_grad():
            negative_prompts = 'deformed eyes, blurry, low quality, deformed, disfigured, extra limbs, watermark, text'#'bad anatomy, bad proportions, blurry, cloned face, cropped, deformed, dehydrated, disfigured, duplicate, error, extra arms, extra fingers, extra legs, extra limbs, fused fingers, gross proportions, jpeg artifacts, long neck, low quality, lowres, malformed limbs, missing arms, missing legs, morbid, mutated hands, mutation, mutilated, out of frame, poorly drawn face, poorly drawn hands, signature, text, too many fingers, ugly, username, watermark, worst quality'
            text_embeddings = self.prompt_to_emb(prompt, negative_prompts)
            latents = self.emb_to_latents(text_embeddings)
            image = self.latents_to_pil(latents)
            image = image[0]
        return image

class ImageCaptioningPipeline:
    def __init__(self, config):
        self.config = config
        self.device = "cuda:0" if torch.cuda.is_available() else "cpu"
        self.torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

        # Load the model and processor
        self.model = AutoModelForCausalLM.from_pretrained(self.config.caption_model, torch_dtype=self.torch_dtype, trust_remote_code=True).to(self.device)
        self.processor = AutoProcessor.from_pretrained(self.config.processor, trust_remote_code=True)
        self.max_new_tokens = config.max_new_tokens
        self.num_beams = config.num_beams
        self.do_sample = config.do_sample
    def load_image(self, file: UploadFile):
        return Image.open(file.file)

    def generate_caption_bbox(self, image, prompt="<OD>"):
        

        # Preprocess inputs
        inputs = self.processor(text=prompt, images=image, return_tensors="pt").to(self.device, self.torch_dtype)

        # Generate output
        generated_ids = self.model.generate(
            input_ids=inputs["input_ids"],
            pixel_values=inputs["pixel_values"],
            max_new_tokens=self.max_new_tokens,
            num_beams=self.num_beams,
            do_sample=self.do_sample
        )
        generated_text = self.processor.batch_decode(generated_ids, skip_special_tokens=False)[0]

        # Post-process the generated text
        parsed_answer = self.processor.post_process_generation(generated_text, task="<OD>", image_size=(image.width, image.height))
        return parsed_answer

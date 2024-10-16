import os
import logging
from dotenv import load_dotenv
import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer

# Load environment variables from the .env file
load_dotenv()

# Load constants from environment variables or set default values
MODEL_NAME = os.getenv("MODEL_NAME") 
MAX_LENGTH = int(os.getenv("MAX_LENGTH"))
NUM_BEAMS = int(os.getenv("NUM_BEAMS"))
DO_SAMPLE = os.getenv("DO_SAMPLE").lower() in ["true", "1", "t"] 
REPETITION_PENALTY = float(os.getenv("REPETITION_PENALTY"))
TOP_K = int(os.getenv("TOP_K"))
TOP_P = float(os.getenv("TOP_P"))
TEMPERATURE = float(os.getenv("TEMPERATURE"))
NO_REPEAT_NGRAM_SIZE = int(os.getenv("NO_REPEAT_NGRAM_SIZE"))

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TextGenerator:
    def __init__(self) -> None:
        """Initialize the text generator by loading the model and tokenizer."""
        logger.info(f"Loading model: {MODEL_NAME}")
        self.tokenizer: GPT2Tokenizer = GPT2Tokenizer.from_pretrained(MODEL_NAME)
        self.model: GPT2LMHeadModel = GPT2LMHeadModel.from_pretrained(MODEL_NAME)
        self.model.eval()
        logger.info("Model and tokenizer loaded successfully.")

    def generate_text(
        self, 
        input_text: str, 
        max_length: int = MAX_LENGTH, 
        num_beams: int = NUM_BEAMS,
        do_sample: bool = DO_SAMPLE,
        repetition_penalty: float = REPETITION_PENALTY,
        top_k: int = TOP_K,
        top_p: float = TOP_P,
        temperature: float = TEMPERATURE,
        no_repeat_ngram_size: int = NO_REPEAT_NGRAM_SIZE
    ) -> str:
        """
        Generate text based on the input text.
        
        Parameters:
            input_text (str): The input text for generation.
            max_length (int): The maximum length of the generated text.
            num_beams (int): The number of beams for beam search.
            do_sample (bool): Whether to sample or use greedy decoding.
            repetition_penalty (float): The penalty for repeated sequences.
            top_k (int): The number of highest probability tokens to consider.
            top_p (float): The probability mass for nucleus sampling.
            temperature (float): Temperature for sampling; higher values = more randomness.
            no_repeat_ngram_size (int): The size of n-grams that cannot be repeated.
        
        Returns:
            str: The generated text.
        """
        logger.info(f"Generating text for input: '{input_text}'")
        input_ids = self.tokenizer.encode(input_text, return_tensors='pt')
        
        with torch.no_grad():
            output = self.model.generate(
                input_ids,
                max_length=max_length,
                num_beams=num_beams,
                do_sample=do_sample,
                repetition_penalty=repetition_penalty,
                top_k=top_k,
                top_p=top_p,
                temperature=temperature,
                no_repeat_ngram_size=no_repeat_ngram_size
            )
        
        generated_text = self.tokenizer.decode(output[0], skip_special_tokens=True)
        logger.info(f"Generated text: '{generated_text}'")
        return generated_text

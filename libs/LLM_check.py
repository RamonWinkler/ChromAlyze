from haystack import Pipeline
from haystack.components.builders.prompt_builder import PromptBuilder
from haystack.components.generators import HuggingFaceAPIGenerator
from haystack.utils import Secret
from typing import Optional

class TextRestructurer:
    def __init__(self, api_key: Optional[str] = None, model: str = "HuggingFaceH4/zephyr-7b-beta"):
        """
        Initialize the TextRestructurer with a pipeline.
        
        :param api_key: HuggingFace API key
        :param model: HuggingFace model to use
        """
        # Prompt template for text restructuring
        template = """
        Rewrite the following text short, and friendly, and accurate:
        
        {{ text }}
        
        Provide a concise in complete sentences, friendly version that captures the core message.
        """
        
        # Create generator
        self.generator = HuggingFaceAPIGenerator(
            api_type="serverless_inference_api",
            api_params={"model": model},
            token=Secret.from_token(api_key)
        )
        
        # Create pipeline
        self.pipeline = Pipeline()
        self.pipeline.add_component("prompt_builder", PromptBuilder(template=template))
        self.pipeline.add_component("llm", self.generator)
        
        # Connect pipeline components
        self.pipeline.connect("prompt_builder", "llm")

    def restructure_text(self, text: str) -> str:
        """
        Restructure the input text using the configured pipeline.
        
        :param text: Text to be restructured
        :return: Restructured text as a .HTML similar File
        """
        try:
            result = self.pipeline.run({
                "prompt_builder": {"text": text}
            })
            
            # Extract and clean the best reply
            restructured_text = result['llm']['replies'][0]#.strip().strip("_")
            return restructured_text
        
        except Exception as e:
            print(f"Error in text restructuring: {e}")
            return text  # Fallback to original text

    def __str__(self) -> str:
        """
        Provide a string representation of the TextRestructurer.
        
        :return: Description of the text restructuring capabilities
        """
        return "TextRestructurer: AI-powered text restructuring"
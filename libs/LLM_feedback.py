from haystack import Pipeline
from haystack.components.builders.prompt_builder import PromptBuilder
from haystack.components.generators import HuggingFaceAPIGenerator
from haystack.utils import Secret
from typing import Optional

class feedback:
    def __init__(self, api_key: Optional[str] = None, model: str = "HuggingFaceH4/zephyr-7b-beta"):
        # Prompt template for text restructuring
        template = """
        Role: friendly Assistant

        Feedback:{{ feedback }}
        Inform the user that the feedback is received and will be processed.
        Thank the user for the feedback.
        Provide a **short** and **concise** answer.

        Context:
        Application is a Machine learning prediction of coronary heart disease risk using Logistic Regression.
        The report is generated with LLM for user recommendations including lifestyle changes.
        It runs on on a flask API and is hosted on waitress.
        The API has a input form and a report that is generated based on the input form.
        The Metrics of the Machine Learning Model are:
        Accuracy: 0.67
        Precision: 0.25
        Recall: 0.63
        F1 Score: 0.35
        Company: Chromalyze

        
        Exclude:
        Do not provide any risk evaluation.
        Do not provide any medical advice.
        Do not repeat the feedback.

        Answer:

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

    def give_feedback(self, feedback: str) -> str:
        try:
            result = self.pipeline.run({
                "prompt_builder": {"feedback": feedback}
            })
            
            # Extract and clean the best reply
            answer = result['llm']['replies'][0].strip().strip("_")
            return answer
        
        except Exception as e:
            print(f"Error in feedback restructuring: {e}")
            return "thank you for your feedback"  # Fallback to original feedback

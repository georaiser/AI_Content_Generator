from dotenv import load_dotenv
from langchain_core.output_parsers import JsonOutputParser
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from backend.prompts.tone_generator import GENERATE_REFINED_INFO
from backend.prompts.content_generation_prompts import GENERATE_INFO
from backend.src.llm import GroqModelHandler
from backend.models.content_generation_models import (
    ContentGenerationScript,
    ToneGenerationScript,
)
import logging

# Configurar logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

class ContentGenerator:
    def __init__(self):
        """Initialize the Groq model handler"""
        groq_handler = GroqModelHandler()
        self.llm = groq_handler.get_llm()

    def create_parser(self):
        """Create a JsonOutputParser for ContentGenerationScript"""
        return JsonOutputParser(pydantic_object=ContentGenerationScript)

    def create_tone_parser(self):
        """Create a JsonOutputParser for ToneGenerationScript"""
        return JsonOutputParser(pydantic_object=ToneGenerationScript)

    def create_script_chain(self, template, parser, input_variables):
        """Create a PromptTemplate with the template, input_variables and format_instructions"""
        reduce_prompt = PromptTemplate(
            template=template,
            input_variables=input_variables,
            partial_variables={"format_instructions": parser.get_format_instructions()},
        )
        # Create a LLMChain with the model, the prompt and the parser
        chain = LLMChain(llm=self.llm, prompt=reduce_prompt, output_parser=parser)
        return chain

    def generate_text(self, info):
        """Generate text based on the input information"""
        parser = self.create_parser()
        content_chain = self.create_script_chain(
            template=GENERATE_INFO,
            parser=parser,
            input_variables=[
                "title",
                "price",
                "description",
                "additional_info",
                "available_sizes",
                "image_description",
            ],
        )
        # Invoke the chain
        content_chain_invoke = content_chain.invoke(
            {
                "title": info["title"],
                "price": info["price"],
                "description": info["description"],
                "available_sizes": info["available_sizes"],
                "additional_info": info["additional_info"],
                "image_description": info["image_description"],
            }
        )

        # Log the raw response for debugging
        logger.info(f"Raw LLM response: {content_chain_invoke}")

        return content_chain_invoke["text"]["content"]

    def apply_tone(self, script, target_audience, tone, language):
        # Create the tone parser
        parser_tone = self.create_tone_parser()
        # Create the tone generation chain
        generation_chain = self.create_script_chain(
            template=GENERATE_REFINED_INFO,
            parser=parser_tone,
            input_variables=[
                "previous_script",
                "target_audience",
                "tone",
                "language",
            ],
        )
        # Invoke the chain with the script, audience, tone and language
        chain_invoke = generation_chain.invoke(
            {
                "previous_script": script,
                "target_audience": target_audience,
                "tone": tone,
                "language": language,
            }
        )
        return chain_invoke

    def generate_content(self, metadata, target_audience, tone, language):
        # Generate the initial text
        generated_text = self.generate_text(metadata)
        # Log the generated text
        logger.info(f"generate_content from content_generator.py: {generated_text}")
        # Apply the tone to the generated text
        # generated_text_tone = self.apply_tone(
        #     generated_text["content"], target_audience, tone, language
        # )
        # # Log the generated text with tone
        # logger.info(f"generated_text_tone: {generated_text_tone}")
        # # Return the final generated text with tone
        # return generated_text_tone
        return generated_text

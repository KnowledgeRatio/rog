import json
import asyncio
from llm_axe.agents import OnlineAgent  # LLM-axe library for internet-connected capabilities
from llm_axe.models import OllamaChat    # Ollama chat model connector for llm-axe
import semantic_kernel as sk             # Microsoft's Semantic Kernel framework
from semantic_kernel.connectors.ai.ollama import OllamaChatCompletion, OllamaTextEmbedding  # Semantic Kernel's Ollama connectors

class SemanticKernelBridge:
    """
    Bridge class that combines Semantic Kernel capabilities with llm-axe internet connectivity.
    
    This class serves as the central integration point between:
    1. Microsoft's Semantic Kernel for orchestration and plugins
    2. llm-axe for internet connectivity and online research
    3. Ollama for local LLM inference
    
    The bridge enables both online and offline analysis with a unified interface.
    """
    def __init__(self, model_name="rog-research-preview"):
        """
        Initialize the bridge with necessary components.
        
        Args:
            model_name (str): Name of the Ollama model to use (default: "rog-research-preview")
        """
        # Initialize llm-axe components for internet access
        self.llm = OllamaChat(model=model_name)
        self.online_agent = OnlineAgent(self.llm)
        self.model_name = model_name
        
        # Initialize Semantic Kernel components
        self.kernel = sk.Kernel()
        # Configure the OllamaChatCompletion service for Semantic Kernel
        ollama_service = OllamaChatCompletion(
            ai_model_id=model_name,
            service_id="ollama-chat"
        )
        # Set the base URL for the Ollama API
        ollama_service.client.base_url = "http://localhost:11434"
        self.kernel.add_service(ollama_service)
        
    def run_semantic_kernel_query(self, prompt):
        """
        Run a query through the Python Semantic Kernel implementation.
        
        Uses the Semantic Kernel to process a prompt through the local Ollama model.
        
        Args:
            prompt (str): The prompt to send to the model
            
        Returns:
            str: The result from the Semantic Kernel
        """
        try:
            # Create an async function to handle the prompt execution
            async def execute_prompt():
                result = await self.kernel.invoke_prompt(prompt, service_id="ollama-chat")
                return str(result)
            
            # Set up the event loop for async execution
            try:
                # Try to get the current event loop
                loop = asyncio.get_event_loop()
            except RuntimeError:
                # If there's no event loop in this thread, create a new one
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
            
            # Run the async function in the event loop
            result = loop.run_until_complete(execute_prompt())
            return result
                
        except Exception as e:
            print(f"Error in Semantic Kernel query: {str(e)}")
            return f"Error analyzing content: {str(e)}"
    
    def verify_content_with_internet(self, content_text):
        """
        Verify content using llm-axe's internet access capability.
        
        This maintains the existing functionality while adding Semantic Kernel capabilities.
        Uses the online_agent from llm-axe to search the internet for information.
        
        Args:
            content_text (str): The content to verify
            
        Returns:
            str: Analysis result with internet-based verification
        """
        prompt = f"Please verify whether the following content is authentic or contains disinformation. Use the internet to find relevant information and provide evidence-based analysis:\n\n{content_text}"
        return self.online_agent.search(prompt)
    
    def create_unified_analysis(self, local_analysis, internet_analysis, content_text):
        """
        Create a unified analysis by combining local and internet-based analyses.
        
        Merges the results of two separate analyses into a cohesive verification report.
        
        Args:
            local_analysis (str): Analysis based on internal model knowledge
            internet_analysis (str): Analysis based on internet search results
            content_text (str): The original content being analyzed
            
        Returns:
            str: A synthesized analysis combining both perspectives
        """
        unification_prompt = f"""
You have two separate analyses of the following content:
-----------------
{content_text}
-----------------

LOCAL ANALYSIS (based on internal knowledge):
{local_analysis}

INTERNET-BASED ANALYSIS (with web search results):
{internet_analysis}

Please synthesize these two analyses into a single, coherent verification report, keep it succinct and without duplication. 
You should consider both the internal knowledge patterns and the internet-based evidence, but you do not need to illustrate to the user the split between the two sources.
The user cares about the results, not which of the two origins they derive.
Resolve any contradictions between the two analyses.
Provide a final authenticity assessment based on the combined evidence.
Format your response as a complete verification report with a clear conclusion.
"""
        return self.run_semantic_kernel_query(unification_prompt)
    
    def enhanced_verification(self, content_text):
        """
        Enhanced verification that uses both Semantic Kernel and llm-axe.
        
        This is the main verification method that combines all capabilities:
        1. Local model knowledge via Semantic Kernel
        2. Internet search via llm-axe
        3. Unified analysis combining both perspectives
        
        Args:
            content_text (str): The content to verify
            
        Returns:
            dict: Dictionary containing all analyses:
                - semantic_kernel_analysis: The local analysis result
                - internet_verification: The internet-based analysis
                - combined_result: The final unified analysis
        """
        # First use Semantic Kernel for initial analysis
        sk_prompt = f"Analyze the following content and identify potential disinformation patterns or concerns using only your internal knowledge:\n\n{content_text}"
        initial_analysis = self.run_semantic_kernel_query(sk_prompt)
        
        # Then use llm-axe to verify with internet access
        online_prompt = f"Please verify the following content using internet resources only. Provide evidence-based analysis with citations:\n\n{content_text}"
        online_verification = self.online_agent.search(online_prompt)
        
        # Create a unified analysis that combines both perspectives
        unified_analysis = self.create_unified_analysis(initial_analysis, online_verification, content_text)
        
        # Return a dictionary with all analyses
        return {
            "semantic_kernel_analysis": initial_analysis,
            "internet_verification": online_verification,
            "combined_result": unified_analysis
        }

# Example usage when the file is run directly
if __name__ == "__main__":
    bridge = SemanticKernelBridge()
    result = bridge.enhanced_verification("The Earth is flat and this has been proven by scientists.")
    print(result["combined_result"])
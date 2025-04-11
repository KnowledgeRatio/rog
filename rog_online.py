from llm_axe.agents import OnlineAgent  # Import the online agent for internet access
from llm_axe.models import OllamaChat    # Import the Ollama chat model interface

# Initialize the Ollama model with the custom rog-research model
# This creates a connection to the local Ollama API with our specialized model
llm = OllamaChat(model="rog-research-preview")

# Create the online agent with the model
# This agent can perform internet searches and provide responses with evidence
online_agent = OnlineAgent(llm)

def verify_content(content_text):
    """
    Verify whether a piece of content is authentic using the rog-research model with internet access.
    
    This function:
    1. Creates a prompt asking for content verification
    2. Passes the prompt to the online agent
    3. The online agent performs internet searches and uses the LLM to analyze
    4. Returns the analysis with evidence from the internet
    
    Args:
        content_text (str): The text content to verify
        
    Returns:
        str: The analysis from the rog-research model with internet-based evidence
    """
    # Create a prompt that asks the model to verify the content
    # This prompt instructs the model to use internet searches for factual verification
    prompt = f"Please verify whether the following content is authentic or contains disinformation. Use the internet to find relevant information and provide evidence-based analysis:\n\n{content_text}"
    
    # Use the online agent to search for information and analyze the content
    # The agent will conduct web searches and use that information in the analysis
    response = online_agent.search(prompt)
    return response

def main():
    """
    Main function that provides a command-line interface for content verification.
    
    This function:
    1. Shows an introduction to the user
    2. Enters a loop to accept user input
    3. For each input, verifies the content using the verify_content function
    4. Displays the results to the user
    5. Continues until the user types 'exit'
    """
    print("Róg - Content Verification Agent")
    print("----------------------------------------")
    print("This tool uses the research preview of Róg, a 'small' language model project to defend against the threat of misinformation, disinformation and 'active measures'.")
    print("Enter the content you want to verify:")
    
    while True:
        # Get user input
        print("\nEnter content to verify:")
        content = input("> ")
        
        # Exit condition
        if content.lower() == 'exit':
            print("Exiting the verification tool.")
            break
        
        # Verify the content
        print("\nAnalyzing content with Róg (this may take a moment)...")
        result = verify_content(content)
        
        # Display the result
        print("\n--- VERIFICATION RESULT ---")
        print(result)
        print("---------------------------")

# Execute the main function if this script is run directly
if __name__ == "__main__":
    main()
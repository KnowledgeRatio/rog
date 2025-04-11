// semantic-kernel-ollama.js - Integration of Semantic Kernel with Ollama models
// Provides standalone JavaScript-based Semantic Kernel functionality

import { Kernel, FunctionCallingKernelPlugin } from "@microsoft/semantic-kernel";  // Semantic Kernel core functionality
import { OllamaTextCompletionService } from "@microsoft/semantic-kernel-connectors-ollama";  // Ollama connector for SK

/**
 * Demonstrates how to run Semantic Kernel with Ollama models
 * 
 * This function:
 * 1. Sets up a connection to the local Ollama API
 * 2. Creates a Semantic Kernel instance with the Ollama service
 * 3. Defines a simple question-answering function
 * 4. Demonstrates the function with a sample question
 */
async function runSemanticKernelWithOllama() {
  try {
    // Configure the Ollama endpoint (same as your existing setup)
    const ollamaEndpoint = "http://localhost:11434";
    const modelName = "rog-research-preview"; // Use your custom model
    
    // Create an instance of the Ollama text completion service
    // This connects Semantic Kernel to the local Ollama API
    const ollamaTextCompletionService = new OllamaTextCompletionService(modelName, ollamaEndpoint);
    
    // Create a kernel builder
    const builder = Kernel.builder();
    
    // Add the Ollama text completion service to the kernel
    // This registers the Ollama service with the "ollama" service ID
    const kernel = builder.withAIService("ollama", ollamaTextCompletionService).build();
    
    console.log("Semantic Kernel with Ollama initialized successfully!");
    
    // Example: Create a function to generate text using your Ollama model
    /**
     * Asks a question to the Ollama model through Semantic Kernel
     * 
     * @param {string} question - The question to ask the model
     * @returns {string} - The model's response
     */
    async function askQuestion(question) {
      console.log(`Question: ${question}`);
      const result = await kernel.invokePromptAsync(question);
      console.log(`Answer: ${result.value}`);
      return result.value;
    }
    
    // Test with a sample question
    // This demonstrates basic functionality of the integration
    await askQuestion("Why is the sky blue?");

    // You can build more complex interactions using Semantic Kernel's features
    // while maintaining compatibility with your llm-axe Python integration
    
  } catch (error) {
    console.error("Error in Semantic Kernel Ollama integration:", error);
  }
}

// Run the example
// This is the main execution point for this script
runSemanticKernelWithOllama();
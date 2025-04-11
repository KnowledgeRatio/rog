// semantic_kernel_query.js - Script to handle Semantic Kernel queries from Python bridge
// This file provides JavaScript-based Semantic Kernel functionality for the Rog Research project

import fs from 'fs';  // File system module for reading/writing files
import { Kernel } from "@microsoft/semantic-kernel";  // Semantic Kernel core functionality
import { OllamaTextCompletionService } from "@microsoft/semantic-kernel-connectors-ollama";  // Ollama connector for Semantic Kernel

/**
 * Processes a query using Semantic Kernel with an Ollama model
 * 
 * This function:
 * 1. Reads a prompt from a temporary file
 * 2. Initializes Semantic Kernel with an Ollama service
 * 3. Processes the prompt using the Ollama model
 * 4. Returns the result as JSON for the Python bridge to parse
 */
async function processQuery() {
  try {
    // Read the prompt from the temporary file
    // This file is created by the Python bridge to pass prompts to JavaScript
    const inputData = JSON.parse(fs.readFileSync('temp_prompt.json', 'utf8'));
    const prompt = inputData.prompt;
    
    if (!prompt) {
      console.error('No prompt provided in input file');
      process.exit(1);
    }

    // Configure the Ollama endpoint
    const ollamaEndpoint = "http://localhost:11434";
    const modelName = "rog-research-preview"; // Use the custom Rog Research model
    
    // Create an instance of the Ollama text completion service
    const ollamaTextCompletionService = new OllamaTextCompletionService(modelName, ollamaEndpoint);
    
    // Create a kernel builder and add the Ollama service
    const builder = Kernel.builder();
    const kernel = builder.withAIService("ollama", ollamaTextCompletionService).build();
    
    // Process the query using Semantic Kernel
    // This invokes the Ollama model with the provided prompt
    const result = await kernel.invokePromptAsync(prompt);
    
    // Output the result as JSON for the Python bridge to parse
    // This allows seamless integration between Python and JavaScript components
    console.log(JSON.stringify({ result: result.value }));
    
    // Clean up the temporary file after processing
    try {
      fs.unlinkSync('temp_prompt.json');
    } catch (err) {
      // Ignore errors on cleanup
    }
    
  } catch (error) {
    console.error(`Error processing query: ${error.message}`);
    process.exit(1);
  }
}

// Run the query processor
// This is the main execution point for this script
processQuery();
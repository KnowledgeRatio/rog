// Script to build and test a custom Ollama model for the Rog Research project
// This script creates a custom LLM model using the Ollama framework and tests it with a sample query

const { execSync } = require('child_process');  // Used to execute shell commands
const fetch = require('node-fetch');            // Used for HTTP requests to the Ollama API
const fs = require('fs');                       // File system operations
const path = require('path');                   // Path manipulation utilities

/**
 * Builds the custom "rog-research" Ollama model using the Modelfile
 * 
 * @returns {Promise<boolean>} - Returns true if model was built successfully, false otherwise
 */
async function buildModel() {
  try {
    console.log('Building custom Ollama model "rog-research"...');
    const modelfilePath = path.resolve(__dirname, 'Modelfile');
    
    // Check if the Modelfile exists before attempting to build
    if (!fs.existsSync(modelfilePath)) {
      throw new Error('Modelfile not found in the current directory');
    }
    
    // Build the model using the Ollama CLI command
    const result = execSync('ollama create rog-research -f Modelfile', { encoding: 'utf-8' });
    console.log(result);
    
    return true;
  } catch (error) {
    console.error('Error building the model:', error.message);
    return false;
  }
}

/**
 * Tests the "rog-research" model with a sample disinformation query
 * 
 * Sends a request to the local Ollama API endpoint and displays the model's response
 */
async function testModel() {
  try {
    console.log('Testing rog-research model with a sample query...');
    // Make an API call to the local Ollama server
    const response = await fetch('http://localhost:11434/api/generate', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      // Send a test prompt to evaluate a potentially misleading headline
      body: JSON.stringify({
        model: 'rog-research',
        prompt: 'Review this headline: "Scientists discover that drinking coffee extends lifespan by 20 years"',
        stream: false  // Get complete response at once instead of streaming
      }),
    });

    const data = await response.json();
    console.log('Model Response:');
    console.log(data.response);
  } catch (error) {
    console.error('Error testing the model:', error.message);
  }
}

/**
 * Main execution function
 * 
 * Builds the model first, and if successful, proceeds to test it
 */
async function main() {
  const success = await buildModel();
  if (success) {
    await testModel();
  }
}

// Execute the main function
main();
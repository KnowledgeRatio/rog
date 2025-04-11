// Simple test script to verify Ollama API connectivity and functionality
// This script sends a basic query to the Ollama API to ensure it's working correctly

const fetch = require('node-fetch');  // Used for HTTP requests to the Ollama API

/**
 * Tests connectivity to the Ollama API by sending a simple query
 * 
 * Sends a request to the local Ollama server with a basic prompt
 * and logs the response to verify proper operation
 */
async function testOllama() {
  try {
    // Make a POST request to the Ollama API endpoint
    const response = await fetch('http://localhost:11434/api/generate', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      // Send a simple test prompt to the 'phi' model
      body: JSON.stringify({
        model: 'phi',  // Using the base phi model rather than our custom model
        prompt: 'Why is the sky blue?',  // Simple factual question
        stream: false  // Get complete response at once instead of streaming
      }),
    });

    const data = await response.json();
    console.log('Ollama response:', data);
  } catch (error) {
    console.error('Error connecting to Ollama:', error.message);
  }
}

// Execute the test function
testOllama();
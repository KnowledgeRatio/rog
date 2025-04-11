from flask import Flask, render_template, request, jsonify  # Flask web framework
import os
from semantic_kernel_bridge import SemanticKernelBridge  # Import our custom bridge class

# Initialize Flask application
app = Flask(__name__)

# Initialize our Semantic Kernel bridge that maintains llm-axe internet connectivity
# This creates an instance of our bridge that will be used for all verification requests
bridge = SemanticKernelBridge(model_name="rog-research-preview")

@app.route('/')
def index():
    """
    Route for the main page of the web application.
    
    Returns:
        Rendered HTML template for the main page
    """
    return render_template('index.html')

@app.route('/verify', methods=['POST'])
def verify():
    """
    Enhanced verification endpoint that combines Semantic Kernel and llm-axe.
    
    This is the primary endpoint for content verification, which:
    1. Uses local model knowledge and patterns via Semantic Kernel
    2. Performs internet searches for factual verification via llm-axe
    3. Combines both analyses for a comprehensive result
    
    Returns:
        JSON response containing the unified verification result
    """
    data = request.get_json()
    content = data.get('content', '')
    
    if not content:
        return jsonify({'error': 'No content provided'}), 400
    
    # Use our enhanced verification that combines Semantic Kernel with llm-axe
    try:
        result = bridge.enhanced_verification(content)
        # Just return the combined result as a single field
        return jsonify({'result': result['combined_result']})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Legacy endpoint that only uses llm-axe for compatibility
@app.route('/verify-legacy', methods=['POST'])
def verify_legacy():
    """
    Legacy verification endpoint that only uses llm-axe.
    
    This endpoint exists for:
    - Backward compatibility
    - Performance comparison
    - Testing purposes
    - Cases where a simpler, internet-only analysis is sufficient
    
    Returns:
        JSON response containing the verification result
    """
    data = request.get_json()
    content = data.get('content', '')
    
    if not content:
        return jsonify({'error': 'No content provided'}), 400
    
    # Use only llm-axe for this endpoint
    try:
        response = bridge.verify_content_with_internet(content)
        return jsonify({'result': response})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    
    # Run the Flask app in debug mode
    # Note: Debug mode should be set to False in production
    app.run(debug=True)
#!/bin/bash

# Pull gemma3 and mistral-small models
echo "Pulling gemma3:27b model..."
ollama pull gemma3:27b

echo "Pulling mistral-small:24b model..."
ollama pull mistral-small:24b

echo "Models have been successfully pulled and are ready to use."
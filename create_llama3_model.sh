#!/bin/bash

# Pull gemma3 and mistral-small models
echo "Pulling gemma3:latest model..."
ollama pull gemma3:latest

echo "Pulling mistral-small:latest model..."
ollama pull mistral-small:latest

echo "Models have been successfully pulled and are ready to use."
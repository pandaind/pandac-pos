#!/bin/bash

# Quick start script for Pandac POS API
echo "🚀 Starting Pandac POS API..."

docker-compose up -d

echo ""
echo "✅ API is running!"
echo "📍 API: http://localhost:8000"
echo "📚 Docs: http://localhost:8000/docs"
echo ""
echo "🧪 Test API:"
echo "   cd newman-tests"
echo "   newman run postman/pandac-pos-collection-comprehensive-fixed.json -e postman/environment.json"
echo ""
echo "🛑 Stop: docker-compose down"

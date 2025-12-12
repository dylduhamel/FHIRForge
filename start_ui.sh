#!/bin/bash
# Start both FastAPI and Streamlit services for FHIRForge

echo "🏥 Starting FHIRForge..."
echo ""

# Check if API is already running
if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null ; then
    echo "FastAPI is already running on port 8000"
else
    echo "Starting FastAPI server..."
    poetry run python run.py &
    API_PID=$!
    sleep 3
    echo "FastAPI started (PID: $API_PID)"
fi

echo ""
echo "Starting Streamlit UI..."
echo ""
echo "Access the UI at: http://localhost:8501"
echo "API docs at: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop both services"
echo ""

# Start Streamlit in foreground
poetry run streamlit run src/ui/streamlit_app.py
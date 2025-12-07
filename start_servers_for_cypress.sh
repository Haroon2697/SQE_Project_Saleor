#!/bin/bash

# ============================================
# Start Backend and Dashboard Servers for Cypress
# ============================================

set -e  # Exit on error

cd /home/haroon/SQE/SQE_Project_Saleor

echo "🚀 Starting servers for Cypress testing..."
echo ""

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Stopping servers..."
    kill $BACKEND_PID 2>/dev/null || true
    kill $DASHBOARD_PID 2>/dev/null || true
    echo "✅ Servers stopped"
    exit 0
}

# Trap Ctrl+C and cleanup
trap cleanup SIGINT SIGTERM

# Activate virtual environment for backend
if [ -d ".venv" ]; then
    source .venv/bin/activate
    echo "✅ Virtual environment activated"
elif [ -d "venv" ]; then
    source venv/bin/activate
    echo "✅ Virtual environment activated"
else
    echo "⚠️  Virtual environment not found, using system Python"
fi

# Start PostgreSQL if not running
if ! pg_isready -h localhost -p 5432 > /dev/null 2>&1; then
    echo "⚠️  PostgreSQL is not running. Please start it first:"
    echo "   sudo systemctl start postgresql"
    echo ""
fi

# Start Backend Server (Port 8000)
echo "📡 Starting Saleor backend server on port 8000..."
python manage.py runserver 0.0.0.0:8000 > backend.log 2>&1 &
BACKEND_PID=$!
echo "   Backend PID: $BACKEND_PID"

# Wait for backend to be ready (max 60 seconds)
echo "   Waiting for backend to start..."
for i in $(seq 1 60); do
    if curl -f http://localhost:8000/graphql/ > /dev/null 2>&1; then
        echo "   ✅ Backend server is ready!"
        break
    fi
    if [ $i -eq 60 ]; then
        echo "   ❌ Backend server did not start in time"
        kill $BACKEND_PID 2>/dev/null || true
        exit 1
    fi
    sleep 1
done

# Start Dashboard Server (Port 9000)
if [ -d "dashboard" ] && [ -f "dashboard/package.json" ]; then
    echo ""
    echo "🎨 Starting Saleor dashboard on port 9000..."
    cd dashboard
    
    # Check if node_modules exists, install if not
    if [ ! -d "node_modules" ]; then
        echo "   Installing dashboard dependencies..."
        if command -v pnpm &> /dev/null; then
            pnpm install || echo "   ⚠️  pnpm install failed"
        else
            npm install || echo "   ⚠️  npm install failed"
        fi
    fi
    
    # Start dashboard (use pnpm if available, otherwise npm)
    # Dashboard vite.config.js is already configured for port 9000
    if command -v pnpm &> /dev/null; then
        echo "   Using pnpm to start dashboard..."
        pnpm dev > ../dashboard.log 2>&1 &
    else
        echo "   Using npm to start dashboard..."
        npm run dev > ../dashboard.log 2>&1 &
    fi
    DASHBOARD_PID=$!
    cd ..
    echo "   Dashboard PID: $DASHBOARD_PID"
    
    # Wait for dashboard to be ready (max 60 seconds)
    echo "   Waiting for dashboard to start..."
    for i in $(seq 1 60); do
        if curl -f http://localhost:9000/ > /dev/null 2>&1; then
            echo "   ✅ Dashboard is ready!"
            break
        fi
        if [ $i -eq 60 ]; then
            echo "   ⚠️  Dashboard did not start in time, but continuing..."
            break
        fi
        sleep 1
    done
else
    echo ""
    echo "⚠️  Dashboard directory not found, skipping dashboard startup"
    echo "   Cypress will only test the backend API"
fi

echo ""
echo "✅ Servers are running!"
echo ""
echo "📊 Server Status:"
echo "   - Backend:  http://localhost:8000"
echo "   - Dashboard: http://localhost:9000"
echo ""
echo "🧪 You can now run Cypress tests:"
echo "   npm run cypress:open    # Interactive mode"
echo "   npm run cypress:run     # Headless mode"
echo ""
echo "Press Ctrl+C to stop all servers"
echo ""

# Keep script running
wait


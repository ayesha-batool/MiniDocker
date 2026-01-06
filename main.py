from web_server import app, socketio, load_existing_containers, background_update
import threading

if __name__ == '__main__':
    # Load existing containers from disk
    print("📦 Loading existing containers...")
    load_existing_containers()
    
    # Start background update thread for real-time status
    threading.Thread(target=background_update, daemon=True).start()
    
    print("=" * 60)
    print("🐳 Mini Docker - Web Dashboard")
    print("=" * 60)
    print("📡 Flask backend server starting...")
    print("🌐 Open your browser and navigate to: http://localhost:5000")
    print("💡 Press Ctrl+C to stop the server")
    print("=" * 60)
    
    # Run Flask-SocketIO server
    try:
        socketio.run(app, host='0.0.0.0', port=5000, debug=False, allow_unsafe_werkzeug=True)
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")


#!/usr/bin/env python3
"""
Setup script for Geopolitical Market Analyzer
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True

def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing dependencies...")
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def create_directories():
    """Create necessary directories"""
    print("📁 Creating directories...")
    
    directories = [
        "data",
        "data/cache",
        "models",
        "logs"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✅ Created directory: {directory}")

def setup_environment():
    """Setup environment variables"""
    print("🔧 Setting up environment...")
    
    env_file = ".env"
    env_example = "env_example.txt"
    
    if not os.path.exists(env_file):
        if os.path.exists(env_example):
            shutil.copy(env_example, env_file)
            print("✅ Created .env file from template")
            print("⚠️  Please edit .env file with your API keys")
        else:
            print("⚠️  No .env template found, please create .env file manually")
    else:
        print("✅ .env file already exists")

def validate_setup():
    """Validate the setup"""
    print("🔍 Validating setup...")
    
    # Check if required files exist
    required_files = [
        "app.py",
        "requirements.txt",
        "src/__init__.py",
        "src/data_collector.py",
        "src/analyzer.py",
        "src/visualizer.py",
        "src/risk_assessor.py"
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Missing files: {missing_files}")
        return False
    
    print("✅ All required files present")
    return True

def run_tests():
    """Run system tests"""
    print("🧪 Running system tests...")
    
    try:
        result = subprocess.run([sys.executable, "test_system.py"], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ System tests passed")
            return True
        else:
            print(f"❌ System tests failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Failed to run tests: {e}")
        return False

def print_next_steps():
    """Print next steps for the user"""
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next Steps:")
    print("1. Edit .env file with your API keys:")
    print("   - OPENAI_API_KEY: Your OpenAI API key")
    print("   - NEWS_API_KEY: Your NewsAPI key (optional)")
    print("\n2. Run the application:")
    print("   streamlit run app.py")
    print("\n3. Open your browser and navigate to:")
    print("   http://localhost:8501")
    print("\n4. For testing, run:")
    print("   python test_system.py")

def main():
    """Main setup function"""
    print("🚀 Setting up Geopolitical Market Analyzer\n")
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Create directories
    create_directories()
    
    # Setup environment
    setup_environment()
    
    # Validate setup
    if not validate_setup():
        print("❌ Setup validation failed")
        return False
    
    # Install dependencies
    if not install_dependencies():
        print("❌ Failed to install dependencies")
        return False
    
    # Run tests
    if not run_tests():
        print("❌ System tests failed")
        return False
    
    # Print next steps
    print_next_steps()
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

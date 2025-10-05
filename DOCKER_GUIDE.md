# 🐳 Voice Bot Docker Guide

This guide explains how to run the Voice Bot using Docker for consistent, cross-platform operation.

## 🎯 Why Docker?

- **Consistent Environment**: Same behavior across macOS, Linux, and Windows
- **No Terminal Issues**: Eliminates VS Code vs iTerm vs Terminal.app differences
- **Isolated Dependencies**: No conflicts with system Python/audio libraries
- **Easy Deployment**: One command to run anywhere
- **Reproducible**: Same setup for all developers

## 🚀 Quick Start

### Prerequisites
- Docker Desktop installed
- Docker Compose (included with Docker Desktop)

### Run Voice Bot

```bash
# Build and run with Docker Compose
docker-compose up --build voice-bot

# Or run directly with Docker
docker build -t voice-bot .
docker run -it --rm voice-bot
```

## 🔧 Platform-Specific Setup

### macOS
```bash
# Use the macOS-optimized service
docker-compose up voice-bot-mac
```

### Linux
```bash
# Use the standard service (includes audio device mounting)
docker-compose up voice-bot
```

### Windows
```bash
# Use the macOS service (similar audio handling)
docker-compose up voice-bot-mac
```

## 🎮 Available Modes

Once the container is running, you can use all the same modes:

```bash
# Manual mode (default in Docker)
python voice_bot.py manual

# Simple mode
python voice_bot.py simple

# Smart mode
python voice_bot.py smart

# Full mode (may be slower in container)
python voice_bot.py full

# Test mode
python voice_bot.py test
```

## 🔧 Customization

### Mount Local Models
```bash
# Use your local models instead of downloaded ones
docker run -it --rm -v $(pwd)/models:/app/models voice-bot
```

### Custom Commands
```bash
# Run specific mode
docker run -it --rm voice-bot python voice_bot.py smart

# Run tests
docker run -it --rm voice-bot python voice_bot.py test
```

## 🐛 Troubleshooting

### Audio Issues
```bash
# Check if audio devices are accessible
docker run -it --rm --privileged voice-bot ls -la /dev/snd/

# Test audio with simple command
docker run -it --rm voice-bot python -c "import pyaudio; print('Audio OK')"
```

### Permission Issues
```bash
# Run with proper permissions
docker run -it --rm --user $(id -u):$(id -g) voice-bot
```

### Network Issues
```bash
# Use host networking
docker run -it --rm --network host voice-bot
```

## 📊 Benefits

### ✅ Advantages
- **Consistent**: Same environment everywhere
- **Isolated**: No system conflicts
- **Portable**: Works on any Docker-enabled system
- **Scalable**: Easy to deploy multiple instances
- **Reproducible**: Same setup for all team members

### ⚠️ Considerations
- **Audio**: May need additional setup for audio devices
- **Performance**: Slightly slower than native (negligible for this use case)
- **Size**: Larger than native installation (~500MB image)

## 🔄 Development Workflow

```bash
# Build image
docker build -t voice-bot .

# Run with live code changes (mount source)
docker run -it --rm -v $(pwd):/app voice-bot

# Run tests in container
docker run -it --rm voice-bot python voice_bot.py test
```

## 🎯 Production Deployment

```bash
# Build production image
docker build -t voice-bot:latest .

# Push to registry
docker tag voice-bot:latest your-registry/voice-bot:latest
docker push your-registry/voice-bot:latest

# Deploy to server
docker pull your-registry/voice-bot:latest
docker run -d --name voice-bot-prod voice-bot:latest
```

## 🆘 Support

If you encounter issues:

1. **Check Docker logs**: `docker logs voice-bot`
2. **Verify audio**: Test with simple audio commands
3. **Check permissions**: Ensure proper device access
4. **Platform-specific**: Use the appropriate service in docker-compose.yml

## 🎉 Ready to Use!

Docker provides a robust, consistent environment for the Voice Bot. No more terminal-specific crashes or environment issues!

```bash
# Start your containerized voice bot now!
docker-compose up --build voice-bot
```

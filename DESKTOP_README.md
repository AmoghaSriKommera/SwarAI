# SwarAI Desktop Application

SwarAI has been converted from a web application to a desktop application using Electron. This allows you to run it as a native desktop app on Windows, macOS, and Linux.

## 🖥️ Desktop Features

- **Native Desktop Experience**: Runs as a standalone application
- **System Integration**: App icon in taskbar/dock
- **Keyboard Shortcuts**: Standard desktop shortcuts (Ctrl+N for new chat, etc.)
- **Window Management**: Minimize, maximize, close like any desktop app
- **No Browser Required**: Runs independently of web browsers

## 🚀 Running the Desktop App

### Development Mode
To run the desktop app in development mode (with hot reloading):

```bash
# From the root directory
npm run desktop-dev

# Or from the frontend directory
cd frontend
npm run electron-dev
```

This will:
1. Start the React development server
2. Wait for it to be ready
3. Launch the Electron desktop app
4. Open developer tools for debugging

### Production Mode
To run the built desktop app:

```bash
cd frontend
npm run build-electron
```

## 📦 Building for Distribution

### Build Installer
To create a distributable installer:

```bash
# From root directory
npm run build-desktop

# Or use the Windows batch script
build-desktop.bat

# Or from frontend directory
cd frontend
npm run dist
```

This creates platform-specific installers in `frontend/dist/`:
- **Windows**: `.exe` installer and portable `.exe`
- **macOS**: `.dmg` disk image
- **Linux**: `.AppImage` portable app

### Build Directory Only (No Installer)
For testing purposes, you can build just the app directory:

```bash
cd frontend
npm run pack
```

## 🎯 Desktop App Structure

```
frontend/
├── electron.js           # Main Electron process
├── build/               # Built React app
├── dist/               # Distribution packages
└── package.json        # Desktop app configuration
```

## ⚙️ Configuration

The desktop app configuration is in `frontend/package.json` under the `"build"` section:

- **App ID**: `com.swarai.app`
- **Product Name**: `SwarAI`
- **Categories**: Productivity (macOS), Office (Linux)
- **Installer**: NSIS for Windows, DMG for macOS, AppImage for Linux

## 🔧 Customization

### App Icon
Replace `frontend/public/favicon.ico` with your custom icon. For better quality:
1. Create icon files: `icon.ico` (Windows), `icon.icns` (macOS), `icon.png` (Linux)
2. Place them in `frontend/build/` after building
3. Update the paths in `frontend/package.json` build configuration

### Window Properties
Edit `frontend/electron.js` to customize:
- Window size and minimum size
- Title bar style
- Menu structure
- Keyboard shortcuts

### Security
The app includes security best practices:
- No Node.js integration in renderer
- Context isolation enabled
- Web security enabled
- Remote module disabled

## 🚨 Troubleshooting

### Common Issues

1. **App won't start**: Ensure backend is running on port 8000
2. **White screen**: Check if React build completed successfully
3. **Missing icon**: Replace placeholder favicon.ico with a valid icon file

### Development Tools
- Press `F12` or `Ctrl+Shift+I` to open DevTools
- Use `Ctrl+R` to reload the app
- Use `Ctrl+Shift+R` to force reload

## 📋 Requirements

- Node.js 16+ for building
- Backend running on localhost:8000
- All frontend dependencies installed (`npm install`)

The desktop app communicates with the same backend API, so ensure your backend is configured and running before launching the desktop application. 
@echo off
echo Building SwarAI Desktop Application...
echo.

cd frontend
echo Installing/updating dependencies...
call npm install

echo.
echo Building React application...
call npm run build

echo.
echo Creating desktop application distribution...
call npm run dist

echo.
echo Build complete! Check the frontend/dist folder for the installer.
pause 
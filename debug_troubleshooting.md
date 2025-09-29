# VS Code Python Debugger Troubleshooting

## Current Configuration
- VS Code version: 1.102.0
- Python extensions: ms-python.python, ms-python.debugpy, ms-python.vscode-pylance
- Virtual environment: venv/Scripts/python.exe

## Debug Configurations
1. **Python: Current File** - Debug any open Python file
2. **Python: Debug app.py** - Debug the main Flask application

## Troubleshooting Steps

### 1. Reload VS Code
- Press `Ctrl+Shift+P`
- Type "Developer: Reload Window"
- Press Enter

### 2. Select Python Interpreter
- Press `Ctrl+Shift+P`
- Type "Python: Select Interpreter"
- Choose: `./venv/Scripts/python.exe`

### 3. Check Extensions
- Press `Ctrl+Shift+X`
- Search for "Python"
- Make sure these are installed and enabled:
  - Python (ms-python.python)
  - Pylance (ms-python.vscode-pylance)

### 4. Test Debugger
1. Open `test_debug.py`
2. Set a breakpoint (click in left margin)
3. Press `F5`
4. Select "Python: Current File"

### 5. Alternative Debugger Types
If "debugpy" doesn't work, try:
- "python" (older debugger)
- "pythonExperimental" (experimental debugger)

### 6. Command Palette Commands
- `Python: Start Debugging`
- `Python: Debug Current File`
- `Python: Debug Flask`

## Error Messages to Check
- "Debug type 'python' is not supported"
- "Debug type 'debugpy' is not supported"
- "Python interpreter not found"

## Manual Debug Test
Run this in terminal to verify Python works:
```bash
venv\Scripts\python.exe test_debug.py
``` 
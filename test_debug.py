#!/usr/bin/env python3
"""
Simple test file to verify VS Code debugger works
"""

def main():
    print("Hello from debug test!")
    x = 10
    y = 20
    result = x + y
    print(f"Result: {result}")
    
    # This is a good place to set a breakpoint
    for i in range(5):
        print(f"Count: {i}")
    
    print("Debug test completed!")

if __name__ == "__main__":
    main() 
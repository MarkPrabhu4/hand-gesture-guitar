import os

print("Current working directory:", os.getcwd())

if os.path.isfile("chord001.wav.mp3"):
    print("✔️ File found in current directory.")
else:
    print("❌ File NOT found in current directory.")

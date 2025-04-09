import pygame
import random
import asyncio
import edge_tts
import os
from dotenv import dotenv_values

# Load environment variables
env_vars = dotenv_values(".env")
AssistantVoice = env_vars.get("AssistantVoice","en-CA-LiamNeural")  # Default to LiamNeural if not found

# Asynchronous function to convert text to speech and save as an audio file
async def TextToAudioFile(text):
    file_path = os.path.join("Data", "speech.mp3")

    # Ensure Data folder exists
    os.makedirs("Data", exist_ok=True)

    # Delete existing file to avoid overwrite issues
    if os.path.exists(file_path):
        os.remove(file_path)

    # Generate and save speech
    communicate = edge_tts.Communicate(text, AssistantVoice, pitch='+5Hz', rate='+13%')
    await communicate.save(file_path)

# Function to play the generated speech file
def play_audio(file_path):
    if not os.path.exists(file_path):
        print("Error: Speech file not found!")
        return False  # Return False if the file does not exist

    try:
        pygame.mixer.init()
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()

        # Wait until audio finishes playing
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

        return True  # Return True if audio played successfully

    except Exception as e:
        print(f"Error playing audio: {e}")
        return False  # Return False if there is an error

    finally:
        pygame.mixer.music.stop()
        pygame.mixer.quit()

# Wrapper function to handle TTS
def TTS(Text, func=lambda r=None: True):
    try:
        # Run async function properly
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(TextToAudioFile(Text))

        # Play the generated speech file
        success = play_audio(os.path.join("Data", "speech.mp3"))

        # Notify function if provided
        if callable(func):
            func(success)

    except Exception as e:
        print(f"Error in TTS: {e}")

# Function to process long text and limit TTS length
def TextToSpeech(Text, func=lambda r=None: True):
    sentences = str(Text).split('.')

    # Predefined responses when the text is too long
    responses = [
        "The rest of the result has been printed to the chat screen, kindly check it out sir.",
        "The rest of the text is now on the chat screen, sir, please check it.",
        "You can see the rest of the text on the chat screen, sir.",
        "The remaining part of the text is now on the chat screen, sir.",
        "Sir, you'll find more text on the chat screen for you to see.",
        "The rest of the answer is now on the chat screen, sir.",
        "Sir, please look at the chat screen, the rest of the answer is there.",
        "You'll find the complete answer on the chat screen, sir.",
        "The next part of the text is on the chat screen, sir.",
        "Sir, please check the chat screen for more information.",
        "There's more text on the chat screen for you, sir.",
        "Sir, take a look at the chat screen for additional text.",
        "You'll find more to read on the chat screen, sir.",
        "Sir, check the chat screen for the rest of the text.",
        "The chat screen has the rest of the text, sir.",
        "There's more to see on the chat screen, sir, please look.",
        "Sir, the chat screen holds the continuation of the text.",
        "You'll find the complete answer on the chat screen, kindly check it out sir.",
        "Please review the chat screen for the rest of the text, sir.",
        "Sir, look at the chat screen for the complete answer."
    ]

    # If the text is very long, only speak part of it and display the rest
    if len(sentences) > 4 and len(Text) >= 250:
        short_text = ".".join(sentences[:2]) + "." + random.choice(responses)
        TTS(short_text, func)
    else:
        TTS(Text, func)

# Main execution loop
if __name__ == "__main__":
    while True:
        try:
            TextToSpeech(input("Enter the text: "))
        except KeyboardInterrupt:
            print("\nExiting...")
            break  # Stop the loop on Ctrl+C

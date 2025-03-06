import cv2
from PIL import Image
import google.generativeai as genai
import speech_recognition as sr
import pyttsx3

# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 180)
engine.setProperty('volume', 1.0)

# Ensure valid voice selection
engine.setProperty('voice', 'com.apple.speech.synthesis.voice.Samantha')

# Initialize Gemini AI
genai.configure(api_key="YOUR API KEY")

# Convert text to speech
def text_to_speech(text):
    engine.say(text)
    engine.runAndWait()

# Recognize speech and return text
def speech_recognition():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)

    try:
        recognized_text = recognizer.recognize_google(audio).lower()
        print("You said:", recognized_text)
        return recognized_text
    except sr.UnknownValueError:
        print("Sorry, I didn't get that.")
        text_to_speech("Sorry, I didn't get that.")
        return None
    except sr.RequestError:
        print("Could not request data.")
        text_to_speech("Could not request data.")
        return None

#Capture an image using the webcam.
def capture_image():
    cap = cv2.VideoCapture(0)
    captured_image = None
    text_to_speech("Press space to capture image")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        cv2.imshow("Camera Feed", frame)
        key = cv2.waitKey(1)
        if key == 32:
            captured_image = frame.copy()
            print("Image Captured")
            text_to_speech("Image Captured")
            break

    cap.release()
    cv2.destroyAllWindows()
    return captured_image

# Process the image and ask Gemini AI based on user input
def analyze_image(image, query):
    if image is None:
        print("No image captured.")
        text_to_speech("No image captured.")
        return

    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(rgb_image)

    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content([f"{query}, only in 30 words", pil_image])

    if response and response.text:
        print("AI Response:", response.text)
        text_to_speech(response.text)
    else:
        print("No response from AI.")
        text_to_speech("No response from AI.")

# Main function to handle the loop and user interaction.
def main():
    while True:
        print("Say 'start' to open the camera, or 'exit' to quit.")
        text_to_speech("Say start to open the camera, or exit to quit.")
        user_command = speech_recognition()

        if user_command:
            if "exit" in user_command:
                print("Exiting the application.")
                text_to_speech("Exiting the application.")
                break
            elif "start" in user_command:
                captured_image = capture_image()
                if captured_image is not None:
                    print("Ask anything about the image.")
                    text_to_speech("Ask anything about the image.")
                    user_query = speech_recognition()

                    if user_query:
                        analyze_image(captured_image, user_query)

                print("Say 'continue' to process another image or 'exit' to quit.")
                text_to_speech("Say continue to process another image or exit to quit.")

                while True:
                    next_action = speech_recognition()
                    if next_action:
                        if "exit" in next_action:
                            print("Exiting the application.")
                            text_to_speech("Exiting the application.")
                            return
                        elif "continue" in next_action:
                            break


if __name__ == "__main__":
    main()



**ClariView - Intelligent Image Interpreter using Gemini AI**
ClariView is an AI-powered Streamlit app that uses Google's Gemini (Generative AI) to interpret and describe uploaded images based on user-defined prompts. The app allows multi-prompt support, language translation, and optional audio narration using gTTS (Google Text-to-Speech).

*Features*
Upload any .jpg, .jpeg, or .png image
Enter custom prompts to instruct the AI how to describe the image
Translate the AI’s response into multiple languages
Listen to generated descriptions via text-to-speech
View your history of image descriptions

*How It Works*
User uploads an image and enters one or more prompts.
The app sends the image and prompt(s) to the Gemini-1.5 Flash model.
The model responds with a detailed description based on the prompt and image.
(Optional) The description is translated and played back using gTTS.
All results are saved in the session history.

*Run the app*
streamlit run app.py

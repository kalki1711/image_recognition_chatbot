import google.generativeai as genai
from pathlib import Path
import streamlit as st
from googletrans import Translator
from gtts import gTTS
import io
import base64
genai.configure(api_key='AIzaSyAAiRRMyb-JMXjKsApOd1r8Le7aJRjMOpg' )
def initialize_model():
    generation_config = {"temperature": 0.9}
    return genai.GenerativeModel("gemini-1.5-flash", generation_config=generation_config)
def generate_content(model, image_path, prompts):
    image_part = {
        "mime_type": "image/jpeg",
        "data": image_path.read_bytes()
    }
    results = []
    for prompt_text in prompts:
        prompt_parts = [prompt_text, image_part]
        response = model.generate_content(prompt_parts)
        if response.candidates:
            candidate = response.candidates[0]
            if candidate.content and candidate.content.parts:
                text_part = candidate.content.parts[0]
                if text_part.text:
                    results.append(f"Prompt: {prompt_text}\nDescription:\n{text_part.text}\n")
                else:
                    results.append(f"Prompt: {prompt_text}\nDescription: No valid content generated.\n")
            else:
                results.append(f"Prompt: {prompt_text}\nDescription: No content parts found.\n")
        else:
            results.append(f"Prompt: {prompt_text}\nDescription: No candidates found.\n")
    return results
def translate_text(text, lang):
    translator = Translator()
    translation = translator.translate(text, dest=lang)
    return translation.text
def text_to_speech(text, lang='en'):
    tts = gTTS(text=text, lang=lang)
    audio_bytes = io.BytesIO()
    tts.write_to_fp(audio_bytes)
    audio_bytes.seek(0)
    return audio_bytes
def audio_to_base64(audio_bytes):
    return base64.b64encode(audio_bytes.read()).decode('utf-8')
def main():
    if "prompts" not in st.session_state:
        st.session_state.prompts = ""
    if "results" not in st.session_state:
        st.session_state.results = []
    if "uploaded_file" not in st.session_state:
        st.session_state.uploaded_file = None
    if "history" not in st.session_state:
        st.session_state.history = []
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Chat: ClariView", "History"])
    if page == "Chat: ClariView":
        st.title("ClariView - Image Interpreter")
        uploaded_file = st.file_uploader("Choose an image file", type=["jpg", "jpeg", "png"])
        if uploaded_file is not None:
            st.session_state.uploaded_file = uploaded_file
            with open("temp_image.jpg", "wb") as f:
                f.write(uploaded_file.getvalue())
            model = initialize_model()
            st.write("Enter prompts (one per line):")
            st.session_state.prompts = st.text_area("Prompts", value=st.session_state.prompts)
            if st.button("Generate Description"):
                prompts = [prompt.strip() for prompt in st.session_state.prompts.split('\n') if prompt.strip()]
                if prompts:
                    image_path = Path("temp_image.jpg")
                    st.session_state.results = generate_content(model, image_path, prompts)
                    st.session_state.history.append({
                        "image": uploaded_file,
                        "results": st.session_state.results
                    })
                else:
                    st.write("Please enter prompt.")
            Path("temp_image.jpg").unlink()
        if st.session_state.uploaded_file and st.session_state.results:
            st.image(st.session_state.uploaded_file, caption='Uploaded Image.', use_column_width=True)
            st.write("Chat - ClariView:")
            for description in st.session_state.results:
                st.write(description)
    elif page == "History":
        st.title("History of Generated Descriptions")
        if st.session_state.history:
            for idx, entry in enumerate(st.session_state.history):
                st.write(f"Entry {idx + 1}")
                st.image(entry["image"], caption=f'Image {idx + 1}', use_column_width=True)
                for description in entry["results"]:
                    st.write(description)
        else:
            st.write("No history available yet.")
if __name__ == "__main__":
    main()

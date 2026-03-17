import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import os
import requests
import io
from dotenv import load_dotenv
import textwrap
import random


# Load environment variables from a .env file
load_dotenv()
ANTROPHIC_API_KEY=os.getenv("ANTROPHIC_API_KEY")

meme_templates = [
    "https://i.imgflip.com/1bij.jpg",
    "https://i.imgflip.com/1otk96.jpg",
    "https://i.imgflip.com/2fm6x.jpg",
    "https://i.imgflip.com/39t1o.jpg",
    "https://i.imgflip.com/1bh3.jpg",
]

def get_random_meme_template():
    return random.choice(meme_templates)

def generate_caption(prompt, style):
    headers = {
        "x-api-key": ANTROPHIC_API_KEY,
        "anthropic-version": "2023-06-01",
        "Content-Type": "application/json"
    }
    data = {
        "model": "claude-haiku-4-5-20251001",
        "max_tokens": 256,
        "system": f"You are a witty meme caption generator. Just add one sentence. Generate a caption in a {style.lower()} style.",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }
    response = requests.post("https://api.anthropic.com/v1/messages", headers=headers, json=data)

    if response.status_code == 200:
        result = response.json()
        caption = result['content'][0]['text'].strip()
        return caption
    else:
        st.error(f"Error generating caption. Status code: {response.status_code}\nResponse: {response.text}")
        return None
    
def overlay_text_on_image(image, text):

    draw = ImageDraw.Draw(image)

    # set base font size based on image width
    base_font_size = max(20, image.width // 20)

    # adjust font size if tesxt is very long
    if len(text) > 100:
        font_size = int(base_font_size * 0.8) # reduce by 80 percent
    else:
        font_size = base_font_size # if the text is not long, just use the base font size

    # load a font
    try:
        font = ImageFont.truetype("C:/Windows/Fonts/seguiemj.ttf", font_size)
    except IOError:
        try:
            font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", font_size)
        except IOError:
            font = ImageFont.load_default(size=font_size)

    # adjust wrap width based on font size and image width
    wrap_width = max(30, int(40 * (base_font_size / font_size)))
    wrapped_text = textwrap.fill(text, width=wrap_width)
    lines = wrapped_text.split("\n")

    # calculate total text block height
    total_text_height = 0
    line_heights = []

    # Loop through each line of text
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        line_height = bbox[3] - bbox[1] #  bottom Y-coordinate of the bbox and the top Y-coordinate
        line_heights.append(line_height)
        total_text_height += line_height

    # adjust Y-position: move text upwards if it is tall
    y = image.height - total_text_height - 20 # increased the margin to 20

    for i, line in enumerate(lines):
        bbox = draw.textbbox((0,0), line, font=font)
        line_width = bbox[2] - bbox[0]
        x = (image.width - line_width) / 2

        outline_range = 2
        for adj in range(-outline_range, outline_range + 1):
            for adj_y in range(-outline_range, outline_range + 1):
                draw.text((x + adj, y + adj_y), line, font=font, fill="black")
        draw.text((x,y), line, font=font, fill="white")
        y += line_heights[i]

    return image

def main():
    st.title("AI Meme Generetor")
    st.write("Generate creative meme caption using Claude API and overlay them on you image!")

    option = st.radio("Choose an option:", {"Upload an image", "Use meme template"})

    if option == "Upload an image":
        uploaded_file = st.file_uploader("Upload an image", type=["png", "jpeg", "jpg"])
        if uploaded_file:
            image = Image.open(uploaded_file)
        else:
            image = None
    else:
        if "template_url" not in st.session_state:
            st.session_state.template_url = get_random_meme_template()

        if st.button("Refresh Meme Image"):
            st.session_state.template_url = get_random_meme_template()
        
        # using a default meme template
        template_url = st.session_state.template_url  # Example URL for a classic meme image
        response = requests.get(template_url)
        image = Image.open(io.BytesIO(response.content))
        st.image(image, caption="Your Meme", use_container_width=True)

    prompt = st.text_input("Enter a prompt for the meme caption: ")
    style = st.selectbox("Choose a caption style: ", ("Witty", "Sarcastic", "Wholesome", "Dark humor"))

    if st.button("Generate Meme"):
        if image is None:
            st.error("Please provide an image or select a meme template!")
        elif not prompt:
            st.error("Please enter a prompt for the caption generation!")
        else:
            with st.spinner("Generation caption..."):
                caption = generate_caption(prompt, style)
            if caption:
                st.subheader("Generated Caption: ")
                st.write(caption)

                # Overlay the caption on the image
                meme_image = overlay_text_on_image(image.copy(), caption)
                st.image(meme_image, caption="Your Meme", use_container_width=True)

                # Allow the uiser to download the Meme
                buffered = io.BytesIO()
                meme_image.save(buffered, format="PNG")
                st.download_button("Download Meme", data=buffered.getvalue(), file_name="meme.png", mime="image/png")

if __name__ == "__main__":
    main()
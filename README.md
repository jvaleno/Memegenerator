# AI Meme Generator

A Streamlit web app that generates meme captions using the Claude API and overlays them on images.

## Features

- Upload your own image or pick a random meme template
- Generate AI-powered captions via Claude (Haiku) in multiple styles: Witty, Sarcastic, Wholesome, or Dark humor
- Caption is overlaid directly on the image with a black outline for readability
- Download the finished meme as a PNG

## Requirements

- Python 3.x
- An [Anthropic API key](https://console.anthropic.com/)

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/memegenerator.git
   cd memegenerator
   ```

2. Install dependencies:
   ```bash
   pip install streamlit pillow requests python-dotenv
   ```

3. Create a `.env` file in the project root:
   ```
   ANTROPHIC_API_KEY=your_api_key_here
   ```

## Running the app

```bash
python -m streamlit run main.py
```

Then open [http://localhost:8501](http://localhost:8501) in your browser.

## Project structure

```
memegenerator/
├── main.py        # Main application
├── .env           # API key (not committed)
└── README.md
```

## Notes

- `.env` should be added to `.gitignore` to avoid exposing your API key.
- On Windows, the app uses system fonts (`seguiemj.ttf` or `arial.ttf`) for text rendering.

simple streamlit app i made to get tags from danbooru and gelbooru, useful for constructing prompts for generating images

Hosted on [Streamlit Cloud](https://boorutags.streamlit.app/)

<img width="821" height="775" alt="image" src="https://github.com/user-attachments/assets/1ccb32f8-e330-4c85-9255-081ab2775fdc" />


## How to run locally:

1.  **Clone repo:**
    ```bash
    git clone https://github.com/shadowblade227/fetch_booru_tags.git
    cd fetch_booru_tags
    ```
2.  **Create virtual environment:**
   
    Linux/macOS:
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```
    Windows:
    ```bash
    python -m venv venv
    venv\Scripts\activate
    ```
4.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
5.  **Run the app:**
    ```bash
    streamlit run main.py
    ```
    App will open in your default browser (typically `http://localhost:8501`).

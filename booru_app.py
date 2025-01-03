import re
import streamlit as st

from danbooru_module import fetch_image_data as fetch_danbooru_data, format_image_data as format_danbooru_data, format_clickable_tags as danbooru_clickable_tags
from gelbooru_module import fetch_image_data as fetch_gelbooru_data, format_image_data as format_gelbooru_data, format_clickable_tags as gelbooru_clickable_tags


def extract_image_id_from_url(url):
    pattern = r"(\d+)"
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    return None


input_col, preview_col = st.columns([2, 1])

with input_col:
    image_id_input = st.text_input("Image ID or URL:")
    source_choice = st.radio(
        "Source:",
        ("Danbooru", "Gelbooru"),
        horizontal=True)


if image_id_input:
    if image_id_input.isdigit():
        image_id = image_id_input
    else:
        image_id = extract_image_id_from_url(image_id_input)

    if image_id:
        with st.spinner("Fetching data..."):
            if source_choice == "Danbooru":
                base_url = "https://danbooru.donmai.us"
                data = fetch_danbooru_data(image_id)
                formatted_data = format_danbooru_data(data)
                preview_image_url = data.get(
                    'large_file_url') or data.get('file_url')
            else:  # Gelbooru
                base_url = 'https://gelbooru.com/index.php'
                auth_params = {
                    'api_key': st.secrets['gelbooru_api_key'],
                    'user_id': st.secrets['gelbooru_user_id']
                }
                data = fetch_gelbooru_data(image_id, base_url, auth_params)
                formatted_data = format_gelbooru_data(
                    data, base_url, auth_params)
                preview_image_url = formatted_data.get('url')

        if "error" in data:
            st.error(data["error"])
        else:
            if "error" in formatted_data:
                st.error(formatted_data["error"])
            else:
                post_url = f"{base_url}/posts/{image_id_input}" if source_choice == "Danbooru" else f"{base_url}?page=post&s=view&id={image_id_input}"
                if source_choice == "Danbooru":
                    st.write(
                        f"**Artist:** {danbooru_clickable_tags(formatted_data['artist'])}")
                    st.write(
                        f"**Character:** {danbooru_clickable_tags(formatted_data['character'])}")
                    st.write(
                        f"**Origin:** {danbooru_clickable_tags(formatted_data['origin'])}")
                    st.write(
                        f"**Tags:** {danbooru_clickable_tags(formatted_data['tags'])}")

                    st.code(formatted_data['prompt'],
                            language='text', wrap_lines=True)
                else:  # Gelbooru
                    st.write(
                        f"**Artist:** {gelbooru_clickable_tags(formatted_data['author'])}")
                    st.write(
                        f"**Character:** {gelbooru_clickable_tags(formatted_data['character'])}")
                    st.write(
                        f"**Origin:** {gelbooru_clickable_tags(formatted_data['origin'])}")
                    st.write(
                        f"**Tags:** {gelbooru_clickable_tags(formatted_data['tags'])}")

                    st.code(formatted_data['prompt'],
                            language='text', wrap_lines=True)

                if preview_image_url:
                    with preview_col:
                        st.image(preview_image_url, use_container_width=True)
    else:
        st.error("Invalid URL or image ID")

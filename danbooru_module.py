import requests

BASE_URL = 'https://danbooru.donmai.us/posts'


def fetch_image_data(image_id, base_url=BASE_URL):
    try:
        response = requests.get(f'{base_url}/{image_id}.json')
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"[ERROR]: Failed to fetch data - {e}"}


def format_image_data(data):
    if "error" in data:
        return data
    
    try:
        character = data.get('tag_string_character', '')
        artist = data.get('tag_string_artist', '')
        origin = data.get('tag_string_copyright', '')
        tags = data.get('tag_string_general', '')

        formatted = {
            "artist": artist.replace(" ", ", ").replace("_", " "),
            "character": character.replace(" ", ", ").replace("_", " "),
            "origin": origin.replace(" ", ", ").replace("_", " "),
            "tags": tags.replace(" ", ", ").replace("_", " "),
        }
        
        prompt_parts = []
        if character:
            prompt_parts.append(formatted["character"])
        if origin:
            prompt_parts.append(formatted["origin"])
        if tags:
            prompt_parts.append(formatted["tags"])

        formatted["prompt"] = ", ".join(prompt_parts)
        
        return formatted
    except KeyError as e:
        return {"error": f"Missing key in API response: {e}"}


def format_clickable_tags(tags):
    tag_list = [tag.strip() for tag in tags.split(",")]
    clickable_tags = [f"[{tag}](https://danbooru.donmai.us/posts?tags={tag.replace(' ', '_')})" for tag in tag_list]
    return f"{', '.join(clickable_tags)}"
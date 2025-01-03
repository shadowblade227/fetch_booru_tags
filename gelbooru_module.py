import requests


def fetch_image_data(image_id, base_url, auth_params):
    try:
        url = f"{base_url}?page=dapi&s=post&q=index&id={image_id}&json=1"
        response = requests.get(url, params=auth_params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"[ERROR]: Failed to fetch image data - {e}"}


def fetch_tag_details(tag_names, base_url, auth_params):
    try:
        tag_query = '+'.join(tag_names)
        tag_query = tag_query.replace(r'&#039;', '%27')
        url = f"{base_url}?page=dapi&s=tag&q=index&names={tag_query}&json=1"
        response = requests.get(url, params=auth_params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"[ERROR]: Failed to fetch tag details - {e}"}


def categorize_tags(tags, base_url, auth_params):
    tag_names = tags.split()
    tag_details = fetch_tag_details(tag_names, base_url, auth_params)

    characters = []
    copyrights = []
    author = []
    general = []
    metadata = []
    
    for tag in tag_details.get('tag', []):
        tag_type = tag.get('type', None)
        tag_name = tag.get('name', '').replace('_', ' ').replace(r'&#039;', "'")
        if tag_type == 4:  # Character
            characters.append(tag_name)
        elif tag_type == 3:  # Copyright
            copyrights.append(tag_name)
        elif tag_type == 1: # Author
            author.append(tag_name)
        elif tag_type == 5: # Metadata
            metadata.append(tag_name)
        else:  # General
            general.append(tag_name)

    return characters, copyrights, general, author, metadata


def format_image_data(data, base_url, auth_params):
    if "error" in data:
        return data
    
    try:
        post = data.get('post', [])
        if not post:
            return {'error': 'No post found!'}
        post_data = data.get('post', [{}])[0]
        image_url = post_data.get('file_url')
        tags = post_data.get('tags', '')
        characters, copyrights, general, author, metadata = categorize_tags(tags, base_url, auth_params)
        
        digit_general_tags = [tag for tag in general if tag[0].isdigit()]
        other_general_tags = [tag for tag in general if not tag[0].isdigit()]

        character_str = ', '.join(characters) if characters else ""
        copyright_str = ', '.join(copyrights) if copyrights else ""
        author_str = ', '.join(author) if author else "Unknown"
        metadata_str = ', '.join(metadata) if metadata else ""
        
        digit_general_str = ', '.join(sorted(digit_general_tags))
        other_general_str = ', '.join(sorted(other_general_tags))

        prompt_parts = [digit_general_str]
        if character_str:
            prompt_parts.append(character_str)
        if copyright_str:
            prompt_parts.append(copyright_str)
        if other_general_str:
            prompt_parts.append(other_general_str)

        prompt = ', '.join(part for part in prompt_parts if part)

        formatted = {
        'url': image_url,
        'author': author_str,
        'character': character_str,
        'origin': copyright_str,
        'metadata': metadata_str,
        'tags': digit_general_str + ", " + other_general_str,
        'prompt': prompt
    }
        return formatted

    except (KeyError, IndexError, TypeError) as e:
        return {"error": f"[ERROR]: Unexpected data format or missing key: {e}"}


def format_clickable_tags(tags):
    tag_list = [tag.strip() for tag in tags.split(",")]
    clickable_tags = [f"[{tag}](https://gelbooru.com/index.php?page=post&s=list&tags={tag.replace(' ', '_')})" for tag in tag_list]
    return f"{', '.join(clickable_tags)}"
import requests

def get_page_current_version(url, auth):
    # Send a GET request to retrieve the page information
    response = requests.get(url, auth=auth)
    # Check if the request was successful
    if response.status_code == 200:
        page_data = response.json()
        # Extract the version number from the response
        return page_data['version']['number']
    else:
        return f"Failed to retrieve page. Status code: {response.status_code}", "Response content:", response.text

def create_url_with_title(base_url, title):
    title = title.replace(" ", "+")
    url = base_url + title
    return url

def create_url_with_id(base_url, id):
    url = base_url + id
    return url

def get_page_id_from_title(url, auth):
    '''
    Use this function if you have the ID but need title
    '''
    # Send a GET request to retrieve the page information
    response = requests.get(url, auth=auth)
    # Check if the request was successful
    if response.status_code == 200:
        page_data = response.json()
        # Extract the version number from the response
        return page_data['id']
    else:
        return f"Failed to retrieve page ID. Status code: {response.status_code}", "Response content:", response.text

def get_page_title_from_id(url, auth):
    '''
    Use this function if you have the title but need ID
    '''
    # Send a GET request to retrieve the page information
    response = requests.get(url, auth=auth)
    # Check if the request was successful
    if response.status_code == 200:
        page_data = response.json()
        # Extract the version number from the response
        return page_data['title']
    else:
        return f"Failed to retrieve page ID. Status code: {response.status_code}", "Response content:", response.text

def create_confluence_base_url(domain):
    base_url = f'https://{domain}.atlassian.net/wiki/rest/api/content/'
    return base_url

def create_update_page_content(version_number: int, body_text: str, title: str, representation: str, obj_type: str = "page"):
    '''
    version_number: needed in order to update it when updating page content
    body_text: string representation of whatever you want to update the page to
    obj_type: Many types of objects are available in confluence, for this function, we will use Page as the default as it is designed to update a page. 
        Page: Represents a Confluence page. You can create, retrieve, update, and delete pages using the API.
        Blog Post: Represents a blog post within Confluence. You can create, retrieve, update, and delete blog posts.
        Space: Represents a Confluence space. You can create, retrieve, update, and delete spaces.
        Attachment: Represents an attachment uploaded to a Confluence page or blog post. You can create, retrieve, update, and delete attachments.
        Comment: Represents a comment on a Confluence page or blog post. You can create, retrieve, update, and delete comments.
        Label: Represents a label applied to a Confluence page, blog post, or space. You can manage labels using the API.
        User: Represents a user in Confluence. You can retrieve user details and manage user permissions.
        Group: Represents a user group in Confluence. You can manage group memberships and permissions.
        Content Permission: Represents permissions applied to Confluence content (pages, spaces, etc.). You can manage content permissions using the API.
        Search: Allows you to perform search queries within Confluence and retrieve search results.
    title: Title for the page, string format
    representation:
        Wiki Markup (wiki): Confluence uses its own wiki markup language. You can represent the page body using wiki markup. This format is useful if you want to create rich content with Confluence-specific formatting.
        Storage Format (storage): This format uses Confluence's native storage format, which includes more detailed information about the content's structure. It allows for fine-grained control over the page content.
        HTML (html): You can use HTML markup to represent the page body. This is useful if you're familiar with HTML and want precise control over the page's formatting.
        Plain Text (plain): You can represent the page body as plain text, which is useful for simple content without formatting.
        Custom Content (custom): You can use custom content representations if you have specific requirements that don't fit the standard formats mentioned above. This allows you to define your own content structure.
    '''
    version_number = get_page_current_version + 1
    # Increment the version number

    page_content = {
        "version": {
        "number": version_number
        },
        "type": obj_type,
        "title": title,
        "body": {
            representation: {
                "value": body_text,
                "representation": representation
            }

        }
    }
    return page_content


def create_new_page_content(body_text: str, title: str, representation: str, space_key, obj_type: str = "page"):
    # Create a dictionary with the page data
    page_data = {
        "type": obj_type,
        "title": title,
        "space": {"key": space_key},
        "body": {
            "storage": {
                "value": body_text,
                "representation": representation
            }
        }
    }
    return page_data

def update_page(auth: tuple, url, content):
    # Send the update request
    response = requests.put(url, json=content, auth=auth, headers={'Content-Type': 'application/json'})
    # Check the response for success
    if response.status_code == 200:
        return "Page updated successfully!"
    else:
        return "Failed to update page. Status code:", response.status_code, response.text

def create_page(space_key, title, page_content, auth: tuple, page_data, url):
    # Define your Confluence authentication headers
    headers = {
        "Content-Type": "application/json",
    }
    # Send a POST request to create the page
    response = requests.post(url, json=page_data, headers=headers, auth=auth)

    # Check the response for success
    if response.status_code == 200:
        print("Page created successfully!")
    else:
        print("Failed to create page. Status code:", response.status_code)
        print("Response content:", response.text)

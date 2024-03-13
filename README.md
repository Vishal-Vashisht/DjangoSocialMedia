# Description
This social media platform is constructed using the Python Django framework as part of a personal learning endeavor.

## Feature
- **Authentication:** Securely sign up, sign in.
- **Comments:** Engage with posts through comments.
- **Posting:** Create, Attach images for a rich experience.
- **Likes:** Express your appreciation by liking posts and comments.
- **Saves:** Easily find the posts you need by saving posts
- **Follow/Unfollow:** Stay updated with others' posts.

## Installation
Follow these steps to set up the Social Media Platform on your local machine:

1. **Clone the repository**:
    ```bash
    git clone git@github.com:Vishal-Vashisht/DjangoSocialMedia.git
    ```

2. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Create sqlite3 db file**
    ```bash

    # Windows command
    type nul > filename.txt

    # Linux command
    touch db.sqlite3
     
     ```

3. **Apply database migrations**:

   ```bash
   python manage.py migrate
   ```

4. **Run the development server**:

   ```bash
   python manage.py runserver
   ```
> [!IMPORTANT]
> You can can change the db to desired db from setting file [Settings](myapp/myapp/settings.py)


## Contributing

Contributions welcome! Open issues or submit pull requests.
# IMAGINARIUM – UNLEASH YOUR CREATIVITY!

#### Video Demo: https://www.youtube.com/watch?v=4OP3vWJCOuw

#### Description:
This README includes an overview of the project, structure of the application, and details about each HTML template used.

Welcome to Imaginarium, a unique social media platform designed specifically for artists to showcase their talents and draw inspiration from a diverse community. In an online landscape often overwhelmed by advertisements and humorous distractions found on larger platforms like Facebook and Instagram, Imaginarium seeks to create a serene and focused environment dedicated solely to the appreciation of art.

To join, artists must register, fostering a sense of community while minimizing the presence of disruptive "internet trolls." The straightforward registration process collects essential information, including the user's name, email, and password. Once registered, users are welcomed to their personalized homepage, where they can eagerly begin uploading their artwork, transforming their creative visions into shareable pieces.

When uploading their creations, users are encouraged to provide a title for their artwork—allowing them to add a personal touch. After sharing, they have the flexibility to edit the title or remove the piece entirely, ensuring complete control over their representation.

Exploration is a vital part of the Imaginarium experience. Users can discover an eclectic array of artworks in the “Explore” section, which features a randomized selection from the community. This dynamic page offers delightful surprises and new inspirations with each visit. By clicking on an engaging image, users can access the artist's profile, showcasing their name, an optional biography, and links to their Instagram and Facebook accounts for easy navigation to their broader online presence. Below this information, a lively carousel rotates through the artist's images, continuously displaying their creative output.

Interaction within Imaginarium is actively encouraged. Artists can engage with one another by liking and leaving thoughtful comments on artworks that resonate with them. To promote a supportive atmosphere, users can easily edit or delete their comments, allowing conversations to evolve over time. Additionally, artwork owners have the authority to remove any unwanted comments on their pieces, ensuring that their creative space remains respectful and aligned with their artistic vision.

## Project Structure

### `app.py`
The main application file that configures Flask, defines routes, and handles primary functionalities:
- **Homepage** (`/`, `/home`): Displays a carousel with recent images, the user’s profile information, and featured images.
- **User Authentication** (`/login`, `/register`, `/logout`): Allows users to log in, register, and log out securely.
- **Profile Management** (`/profile`, `/update_profile`): Lets users view and edit their profiles, including updating their bio, social media links, and profile information.
- **Image Management** (`/upload`, `/upload_image`, `/delete_image`, `/update_image_name`): Allows authenticated users to upload, manage, and delete images.
- **Interactivity** (`/like_image`, `/comment_image`, `/edit_comment`, `/delete_comment`, `/get_comments`): Supports user engagement with images through likes and comments.
- **Exploring Artists** (`/artists`, `/explore`, `/explore_artists`): Displays galleries of all users’ images, letting users discover artwork.
- **Public Profiles** (`/public_profile/<int:user_id>`): Allows visitors to view artists’ public profiles with their artworks and social media links.

### Templates (`templates/` Directory)
This section details the HTML files used for rendering the app’s pages. Unused templates should be removed to keep the codebase clean.

#### **`index.html`**
   - **Routes**: `/`, `/home`
   - **Description**: The homepage for logged-in users, displaying a carousel of images, the user’s profile section, and a list of featured images.

#### **`profile.html`**
   - **Route**: `/profile`
   - **Description**: Displays the user’s profile information with editable fields for updating their name, bio, and social media links.

#### **`login.html`**
   - **Route**: `/login`
   - **Description**: Provides the login form for user authentication.

#### **`register.html`**
   - **Route**: `/register`
   - **Description**: Presents the registration form for new users, allowing them to create accounts.

#### **`upload.html`**
   - **Routes**: `/upload`, `/upload_image`
   - **Description**: Allows users to upload and view their images, with options to delete or rename images. The `upload_image` route also handles new uploads.

#### **`user_gallery.html`**
   - **Route**: `/user_gallery/<int:user_id>`
   - **Description**: Shows an artist’s gallery page, displaying all of their uploaded images with a like count for each.

#### **`artists.html`**
   - **Route**: `/artists`
   - **Description**: Displays a list of images from all users with their respective usernames.

#### **`explore_artists.html`**
   - **Route**: `/explore_artists`
   - **Description**: Showcases images from various artists, with user details for easier discovery.

#### **`explore.html`**
   - **Route**: `/explore`
   - **Description**: A broader gallery view that displays all uploaded images with their associated artists’ usernames.

#### **`public_profile.html`**
   - **Route**: `/public_profile/<int:user_id>`
   - **Description**: Displays a public version of an artist’s profile, with their artworks, bio, and social media links.

### Static Files (`static/`)
Contains CSS and JavaScript files that style and enhance the user interface:
- **CSS files**: Used to style the homepage, profile pages, upload forms, and image galleries.
- **JavaScript files**: Adds interactivity, like enabling AJAX for liking and commenting, and enhancing carousel displays.

### Database (`database.db`)
SQLite3 database file where the application stores user data and image-related data.
- **Tables**:
  - **`users`**: Stores user information, including usernames, emails, and social media links.
  - **`images`**: Stores metadata for uploaded images, like image names, file paths, and associated users.
  - **`comments`**: Saves comments on images.
  - **`likes`**: Tracks likes for each image.

### Uploads Directory (`uploads/`)
Stores image files uploaded by users. This folder is specified as `UPLOAD_FOLDER` in `app.py`, ensuring uploaded files are saved correctly.


Other design considerations: I did try to have a follow section, but with my limited knowledge in coding I was unable to make it work.

Sources: In my code most of the java coding was done by copilot since. The process was me having the idea and asking questions on how to implement each idea to my project.
Copilot also worked as a Check50 my making sure my code was as tight as possible without modifing the essence of my work.

-- Users Table
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    bio TEXT,
    facebook_url TEXT,
    instagram_url TEXT
);

-- Images Table
CREATE TABLE images (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    image_url TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Likes Table
CREATE TABLE likes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    image_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (image_id) REFERENCES images(id) ON DELETE CASCADE,
    UNIQUE (user_id, image_id)  -- Ensures a user can only like an image once
);

-- Comments Table
CREATE TABLE comments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    image_id INTEGER NOT NULL,
    comment_text TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (image_id) REFERENCES images(id) ON DELETE CASCADE
);


tables explained


Explanation of the Tables
Users Table:

id: Unique identifier for each user.
username: Unique username for the user.
email: Unique email for the user.
password_hash: Hashed password for security.
bio: Optional field for the user's biography.
facebook_url and instagram_url: Optional fields for social media links. -- https://simpleicons.org/


Images Table:

id: Unique identifier for each image.
user_id: References the user who uploaded the image.
image_url: The URL or path to the image file.
created_at: Timestamp for when the image was uploaded.


Likes Table:

id: Unique identifier for each like.
user_id: References the user who liked the image.
image_id: References the liked image.
The combination of user_id and image_id is unique to prevent multiple likes by the same user on the same image.


Comments Table:

id: Unique identifier for each comment.
user_id: References the user who made the comment.
image_id: References the image the comment is associated with.
comment_text: The actual comment text.
created_at: Timestamp for when the comment was made.

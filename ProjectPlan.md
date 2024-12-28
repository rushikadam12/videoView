# Video Platform Project

This is a platform for users to upload, view, and interact with videos, similar to platforms like YouTube. The project includes user authentication, video uploads, likes, comments, subscriptions, playlists, tweets, and more. The goal is to build a fully-functional video platform step by step, adding new features as the project evolves.

## Features

### 1. User Authentication & Profile Setup
- **User Registration & Login**: Sign up, log in, password reset, and token-based authentication (JWT).
- **User Profile**: Users can update profile details (e.g., username, avatar, cover image, and more).

### 2. Video Upload and Viewing
- **Video Upload**: Upload video files along with metadata (title, description, thumbnail).
- **Video Viewing**: Watch videos with a user-friendly interface, track watch history.

### 3. Likes and Comments on Videos
- **Likes**: Users can like or dislike videos.
- **Comments**: Users can add comments to videos, which will be displayed alongside them.

### 4. Subscription System
- **Subscriptions**: Users can subscribe to channels (other users).
- **Subscription Management**: Users can view, manage, and unsubscribe from channels.

### 5. Playlists
- **Playlist Creation**: Users can create custom playlists.
- **Playlist Management**: Add/remove videos from playlists.

### 6. Tweet System (Social Interaction)
- **Tweet Posting**: Users can post short messages (tweets), which can be linked to videos, comments, or likes.
- **Likes on Tweets**: Users can like tweets, enabling interactions.

### 7. Notifications (Optional but Recommended)
- **Event Notifications**: Notifications for events like new subscriptions, new content, likes, and comments.

### 8. Search Functionality (Optional but Helpful)
- **Video Search**: Search for videos by title, description, or metadata.
- **User Search**: Search for other users or channels.

## Development Plan

### 1. User Authentication & Profile Setup
- Implement user authentication (sign-up, login, password reset) using JWT.
- Allow users to update their profile details.

### 2. Video Upload and Viewing
- Allow users to upload videos with metadata.
- Display videos in a user-friendly interface for viewing, including history tracking.

### 3. Likes and Comments
- Implement like/dislike functionality for videos.
- Enable commenting on videos with a comment system.

### 4. Subscription System
- Implement a subscription system where users can follow other users (channels).
- Display subscription list on the user's profile.

### 5. Playlists
- Allow users to create playlists and manage videos within them.

### 6. Tweet System
- Implement the tweet system for posting short text content.
- Enable liking of tweets and other social interactions.

### 7. Notifications
- Implement notifications for key events like new content, subscriptions, comments, and more.

### 8. Search Functionality
- Add a search system for both videos and users/channels.

## Development Order

1. **Start with User Authentication and Profile Setup**: Authentication is essential before users can interact with the platform.
2. **Video Upload and Viewing**: Focus on core video upload and viewing features.
3. **Likes and Comments**: Enable interactions with videos through likes and comments.
4. **Subscription System**: Allow users to subscribe to channels and manage subscriptions.
5. **Playlists**: Let users organize videos into playlists.
6. **Tweets and Social Interactions**: Introduce tweets and social interaction functionality.
7. **Notifications**: Add notifications for user activities.
8. **Search**: Implement search functionality for videos and users.

## Setup Instructions

### Prerequisites
1.DjangoREST (for backend development).
2. A database system (e.g., PostgreSQL, MongoDB).
3. A front-end framework/library (e.g., React, Angular).
4. JWT or another authentication library for handling authentication.
5. File storage service (e.g., AWS S3, Cloudinary) for video hosting.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


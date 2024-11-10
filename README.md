
# Reindeer Roundup - Secret Santa Gift Exchange App

## Introduction
The **Reindeer Roundup** is a Flask-based web application that facilitates a Secret Santa gift exchange. Users can create and join gift exchanges, manage participation details, and receive email notifications. The application supports authentication, user management, and a gift exchange mechanism (Secret Santa), integrating MongoDB for data management and various service modules for functionality.

## Installation
1. **Clone the repository**.
2. **Install dependencies** with:
   ```bash
   pip install -r requirements.txt
   ```
3. **Set up environment variables**:
   - Create a `.env` file in the project’s root directory.
   - Add the following variables:
     ```plaintext
     export MONGODB_URI = your_mongodb_uri
     export EMAIL_ID = email_to_send_from
     export EMAIL_PASSWORD = email_token
     export JWT_KEY = your_jwt_secret_key
     export FRONTEND_URL = 'http://localhost:3000' 
     ```
4. **(Optional): Set up frontend**:

   [Reindeer Roundup Frontend](https://github.com/mattespositotech/reindeerRoundupFrontend)

## Usage
Run the app using:
```bash
python app.py
```
The application is configured to allow cross-origin requests from specified domains and provides endpoints for managing users, creating exchanges, and sending notifications.

## Features
- **User Registration & Login**: Allows users to sign up and log in using JWT-based authentication.
- **Secret Santa Management**: Users can join or create a Secret Santa exchange.
- **Email Notifications**: Sends email invites to participants.
- **Template-Based Emails**: Custom HTML email templates to enhance user experience.

## Configuration
- **Environment Variables**: Configure JWT and other sensitive information in the `.env` file.
- **MongoDB Connection**: Modify `MongoDataAccess` to connect to the desired MongoDB instance.

## Dependencies
Key dependencies include:
- **Flask**: For the web framework.
- **Flask-JWT-Extended**: For JWT-based authentication.
- **Flask-CORS**: To handle cross-origin requests.
- **pymongo**: For MongoDB access.

## File Structure
- `app.py`: Main application entry point.
- `dataAccess/`: Manages MongoDB interactions.
- `enums/`: Enumerations for structured data types.
- `mockData/`: Mock data for testing.
- `services/`: Core service functions, including user, encryption, and email services.
- `templates/`: HTML templates for emails.
- `utils/`: Utility modules such as constants and custom exceptions.

## Templates
**Email Templates**:
- `invitation_template.html`: Invitation email for the gift exchange.
- `reset_password_template.html`: Password reset email.
- `reciever_template.html`: Email notifying recipients of their assigned giftee.

## Troubleshooting
- **CORS Issues**: Ensure allowed origins are correctly set in `app.py`.
- **JWT Authentication**: Confirm the `JWT_KEY` environment variable is correctly configured.
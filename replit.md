# Replit Project Documentation

## Overview

This is a Flask-based web application called "Умное Game Bot" (Smart Game Bot) - a Russian-language question game chatbot. The application presents users with different categories of questions in a chat-like interface, allowing them to engage with thought-provoking, strange, or intimate questions. The system includes an admin panel for adding new questions and uses session-based state management.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Template Engine**: Jinja2 templates with Flask
- **UI Framework**: Bootstrap 5.3.0 for responsive design
- **Icons**: Font Awesome 6.0.0 for iconography
- **Styling**: Custom CSS with gradient backgrounds and chat-like interface
- **JavaScript**: Vanilla JavaScript for animations and user interactions

### Backend Architecture
- **Framework**: Flask (Python web framework)
- **Session Management**: Flask sessions with server-side storage
- **Data Storage**: In-memory Python dictionaries (no persistent database)
- **Logging**: Python's built-in logging module

### Key Design Decisions
- **Stateless Session Management**: Uses Flask sessions to maintain chat history and user state
- **In-Memory Data Storage**: Questions are stored in Python dictionaries for simplicity
- **Category-Based Questions**: Questions are organized into three categories: smart, strange, and intimate
- **Chat Interface**: Mimics a messaging app with bot and user message styling

## Key Components

### Application Structure
- `app.py`: Main Flask application with routes and business logic
- `main.py`: Application entry point
- `templates/`: HTML templates for the user interface
- `static/`: CSS and JavaScript assets

### Core Features
1. **Question Categories**: Three types of questions (smart, strange, intimate)
2. **Chat Interface**: Conversational UI with message history
3. **Admin Panel**: Interface for adding new questions
4. **Session Management**: Maintains chat history and user state
5. **Responsive Design**: Mobile-friendly interface

### Routes and Functionality
- `/`: Main chat interface
- `/admin`: Admin panel for question management
- `/ask/<category>`: Question selection endpoint
- `/clear_chat`: Chat history clearing
- `/add_question`: Admin question addition

## Data Flow

1. **User Interaction**: User accesses the main page and sees welcome message
2. **Category Selection**: User chooses a question category (smart/strange/intimate)
3. **Question Display**: System randomly selects and displays a question from the chosen category
4. **Chat History**: All interactions are stored in Flask session
5. **Admin Operations**: Admins can add new questions through the admin panel

### Session Data Structure
- `chat_history`: List of chat messages with timestamps
- User state maintained across requests through Flask sessions

## External Dependencies

### Frontend Dependencies
- **Bootstrap 5.3.0**: CSS framework for responsive design
- **Font Awesome 6.0.0**: Icon library for UI elements

### Backend Dependencies
- **Flask**: Web framework
- **Python Standard Library**: datetime, random, logging, os

### Environment Variables
- `SESSION_SECRET`: Flask session secret key (falls back to development key)

## Deployment Strategy

### Current Setup
- **Development Server**: Flask development server on port 5000
- **Host Configuration**: Configured to run on 0.0.0.0 for accessibility
- **Debug Mode**: Enabled for development

### Production Considerations
- Session secret should be set via environment variable
- Debug mode should be disabled in production
- Consider implementing persistent data storage
- Add proper error handling and logging
- Implement user authentication for admin panel

### Scalability Limitations
- In-memory data storage limits scalability
- Session storage is server-side only
- No database persistence means data loss on restart
- Single-server deployment model

## Technical Notes

### Internationalization
- Application is primarily in Russian language
- UI text and questions are in Russian
- Consider adding i18n support for multi-language deployment

### Security Considerations
- Admin panel has no authentication
- Session secret key needs proper configuration
- Input validation needed for admin question submission
- CSRF protection not implemented

### Future Enhancements
- Database integration for persistent storage
- User authentication system
- Question analytics and usage tracking
- Multi-language support
- API endpoints for mobile app integration
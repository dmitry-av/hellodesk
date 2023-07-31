# Your Application Name

## Introduction

This is an API-driven application that provides a platform for client support and ticket management. It allows clients to register, create tickets, and engage in real-time chat sessions with assigned managers. The application is built using Django, Django Channels for WebSocket communication, and utilizes JWT for authentication.

## API Endpoints

### Admin Panel

- `/admin/`: Provides access to the admin panel.

### User Management

- `/api/register/`: Allows clients to register and create an account.
- `/api/auth/`: Provides JWT token for client authentication.
- `/api/auth/refresh/`: Allows the refreshing of the JWT token.

### Ticket Management

- `/api/tickets/`: Enables clients to create new support tickets.
- `/api/tickets/{int:pk}/`: Provides information about a specific ticket, including the WebSocket chat address (`ws://{domain}/ws/chats/{room id}/`).

### User Information

- `/api/users/{int:pk}/`: Retrieves information about a user, including the WebSocket chat address with their assigned manager.

### Chat Module

The application utilizes the Django Channels library to implement real-time chat functionality. The chat module consolidates all chat rooms for various purposes.

#### Chat with Manager

The chat with the manager works as follows:

1. Upon registration, a random manager is assigned to each client from the pool of available managers.
2. Each client has a "manager chat" field, which is an object from the chat module created during registration.
3. The admin panel provides a link that opens the chat with the assigned manager, allowing communication on behalf of the admin.
4. The chat page is implemented using WebSocket technology (`ws://{domain}/ws/chats/{room id}/`).

### Ticket Support Module

The support module consists of two models:

1. Category: Contains fields for category name and sorting order.
2. Ticket: Includes fields for the category, question topic, question content, and client.

API Endpoints:

- `/api/tickets/`: Allows the creation and retrieval of support tickets. Access is granted to the client, managers, and superusers.

Upon ticket creation, a chat is automatically generated, accessible by the client, assigned manager, and superusers. Access to the chat is also available through a link in the admin panel for the specific ticket.

## Security and Access Control

1. Client data is protected to ensure users can only access their own information.
2. Managers and superusers have full access to all client data.
3. Access to chat sessions is strictly controlled to prevent unauthorized access. Authorization tokens are parsed to enforce security measures.
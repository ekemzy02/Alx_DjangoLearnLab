**This documentation explains how the permissions of the bookshelf app and the groups existing within the app.**

## Model Permissions
- `can_view`: Allows a user to view articles.
- `can_create`: Allows a user to create new articles.
- `can_edit`: Allows a user to edit existing articles.
- `can_delete`: Allows a user to delete articles.

## Groups
- Viewers: Only have `can_view` permission.
- Editors: Have `can_create` and `can_edit` permissions.
- Admins: Have all permissions.

## Views
- Views for creating, editing, deleting, and viewing articles check for the appropriate permissions using `@permission_required` decorator.
------------------------------------------
1.**SECURE_SSL_REDIRECT**: Automatically redirects HTTP traffic to HTTPS.
2.**SECURE_HSTS_SECONDS**: Instructs browsers to only access your site over HTTPS for a specified number of seconds (one year in this case).
3.**SECURE_HSTS_INCLUDE_SUBDOMAINS and SECURE_HSTS_PRELOAD**: Enforces HTTPS on all subdomains and allows the site to be included in HTTP Strict Transport Security (HSTS) preload lists used by browsers.
4.**SESSION_COOKIE_SECURE and CSRF_COOKIE_SECURE**: Ensure cookies are only sent over secure HTTPS connections, preventing interception.
5.**X_FRAME_OPTIONS**: Protects your site from being embedded in a frame on another site (helps prevent clickjacking).
6.**SECURE_CONTENT_TYPE_NOSNIFF**: Ensures that browsers don’t try to guess the content type of a response.
7.**SECURE_BROWSER_XSS_FILTER**: Enables the browser’s built-in XSS filter to help prevent XSS attacks.
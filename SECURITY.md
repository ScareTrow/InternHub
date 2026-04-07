# Security Policy

## Reporting a Vulnerability

If you discover a security issue in InternHub, report it through the repository communication channels as soon as possible.

- Open a GitHub issue with the `security` label for non-sensitive reports.
- If the issue should not be disclosed publicly yet, use a private maintainer contact channel if one is published for the repository.
- Include the affected area, reproduction steps, expected impact, and any suggested mitigation.
- Avoid publishing exploit details before maintainers have had a reasonable opportunity to review and address the issue.

## Security Practices

InternHub currently relies on the following baseline security measures:

- Passwords are hashed before storage.
- JWT-based authentication is used for API access.
- Role-based access control (RBAC) is used to separate student and employer permissions.
- Input validation is enforced through the API schema and request handling layers.
- Application data is stored in PostgreSQL.

## Production Guidance

- HTTPS is required for production deployments.
- Secrets such as JWT signing keys and database credentials should be managed outside the repository.
- Open-source development makes the codebase available for community review and security auditing, which helps improve transparency and resilience over time
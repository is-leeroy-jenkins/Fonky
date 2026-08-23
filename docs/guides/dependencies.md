# Dependencies and Credentials

## Missing dependency

`ModuleNotFoundError` means the Python environment lacks an imported integration package. Install the project requirements before debugging provider credentials.

## Authentication

401/403 responses or provider authentication exceptions usually indicate missing, invalid, expired, or unauthorized credentials.

## Cloud authentication

Cloud providers may use credential chains, OAuth tokens, or service-account files in addition to environment variables.

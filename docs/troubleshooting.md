# Troubleshooting

## Import fails
Run `python -m pip install -r requirements.txt` and retry `python -c "from fonky import fonky"`.

## 401/403
Verify provider credentials and authorization.

## Timeout
Check network access, provider availability, and the method timeout argument.

## Empty scraper output
An empty list can be a valid result when the page contains no matching structure. An exception means the request/extraction path failed.

## Loader failure
Check file existence, permissions, format support, and parser/OCR dependencies.

## Validation error
Read the provider-specific method contract. Several fetchers validate paging, mode, date, coordinate, and result-limit constraints before issuing a request.

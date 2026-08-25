# Cloud & Remote Storage

## Scope

Cloud loaders cover remote documents, provider folders, bucket-backed assets, and speech-to-text ingestion for provider-hosted media.

## Key Operations

| Operation                    | Primary Use                                         |
|------------------------------|-----------------------------------------------------|
| `load_google_drive_file`     | load a single Google Drive file                     |
| `load_google_drive_folder`   | load folder content from Google Drive               |
| `load_onedrive`              | load from Microsoft OneDrive                        |
| `load_google_cloud_file`     | load a Google Cloud file object                     |
| `load_aws_file`              | load an AWS-hosted file object                      |
| `load_google_bucket`         | load from a Google Cloud bucket                     |
| `load_aws_bucket`            | load from an S3-compatible bucket                   |
| `load_google_speech_to_text` | transcribe provider-backed audio through Google STT |

## Workflow Patterns

- locate remote asset
- resolve credentials and provider library
- load to text or documents
- preserve metadata for provenance and downstream indexing

## Notes

Cloud loaders are still ingestion workflows. Use them when the asset lives remotely but the target output is a normalized document set.

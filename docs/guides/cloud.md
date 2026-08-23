# Cloud & Remote Storage

Use the Cloud domain when the source document or audio is stored outside the local filesystem.

## Capability Selection

| Source | Function | Authentication Pattern |
|---|---|---|
| Google Drive file | `load_google_drive_file()` | Google Drive OAuth/service credentials |
| Google Drive folder | `load_google_drive_folder()` | Google Drive OAuth/service credentials |
| OneDrive | `load_onedrive()` | Microsoft/O365 credentials or token flow |
| Google Cloud Storage file | `load_google_cloud_file()` | GCP project + application/service credentials |
| Google Cloud Storage bucket | `load_google_bucket()` | GCP project + credentials |
| AWS S3 object | `load_aws_file()` | AWS credential chain or explicit keys |
| AWS S3 bucket/prefix | `load_aws_bucket()` | AWS credential chain or explicit keys |
| Speech-to-Text | `load_google_speech_to_text()` | GCP project + Speech API credentials |

## Workflow — Load a Single S3 Object

```python
from fonky import fonky

documents = fonky.load_aws_file(
    bucket='analysis-data',
    key='reports/quarterly-report.pdf',
    region_name='us-east-1'
)
```

Prefer the ambient AWS credential chain in production rather than passing access keys directly.

## Workflow — Load a Folder from Google Drive

```python
from fonky import fonky

documents = fonky.load_google_drive_folder(
    folder_id='1AbCdEf...',
    recursive=True
)
```

Use recursive loading only when nested folders are intentional; it can materially increase retrieval
volume and processing time.

## Workflow — Transcribe an Audio File

```python
from fonky import fonky

transcript = fonky.load_google_speech_to_text(
    project_id='my-gcp-project',
    file_path='meeting.wav',
    config={
        'language_code': 'en-US'
    }
)
```

## Operational Notes

- Distinguish **SDK/import errors** from **authentication errors**.
- Cloud folder/bucket calls can return large result sets; use prefixes/folder IDs deliberately.
- Credential files and secrets are deployment configuration and should not be committed.
- Network transfer cost and memory consumption can dominate large-object workflows.

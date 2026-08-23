# Cloud

Google Drive, Google Cloud Storage, AWS S3, OneDrive, and Google Speech-to-Text ingestion.

## Functional Operations

| Function | Signature | Purpose |
|---|---|---|
| `load_google_drive_file()` | `load_google_drive_file( file_id: str, recursive: bool = False ) -> Any` | Load a provider file. Provides direct module-level access to ``GoogleDriveLoader.load_file`` using a fresh ``GoogleDriveLoader`` instance. Any: Value returned by ``GoogleDriveLoader.load_file``. |
| `load_google_drive_folder()` | `load_google_drive_folder( folder_id: str, recursive: bool = False ) -> Any` | Load provider folder content. Provides direct module-level access to ``GoogleDriveLoader.load_folder`` using a fresh ``GoogleDriveLoader`` instance. Any: Value returned by ``GoogleDriveLoader.load_folder``. |
| `load_onedrive()` | `load_onedrive( drive_id: str, folder_path: Optional[str] = None, object_ids: Optional[List[str]] = None, auth_with_token: bool = True ) -> Any` | Load source content. Provides direct module-level access to ``OneDriveDocLoader.load`` using a fresh ``OneDriveDocLoader`` instance. Any: Value returned by ``OneDriveDocLoader.load``. |
| `load_google_cloud_file()` | `load_google_cloud_file( project_name: str, bucket: str, blob: str ) -> Any` | Load source content. Provides direct module-level access to ``GoogleCloudFileLoader.load`` using a fresh ``GoogleCloudFileLoader`` instance. Any: Value returned by ``GoogleCloudFileLoader.load``. |
| `load_aws_file()` | `load_aws_file( bucket: str, key: str, aws_access_key_id: Optional[str] = None, aws_secret_access_key: Optional[str] = None, aws_session_token: Optional[str] = None, region_name: Optional[str] = None ) -> Any` | Load source content. Provides direct module-level access to ``AwsFileLoader.load`` using a fresh ``AwsFileLoader`` instance. Any: Value returned by ``AwsFileLoader.load``. |
| `load_google_speech_to_text()` | `load_google_speech_to_text( project_id: str, file_path: str, config: Optional[Dict[str, Any]] = None ) -> Any` | Load source content. Provides direct module-level access to ``GoogleSpeechToTextLoader.load`` using a fresh ``GoogleSpeechToTextLoader`` instance. Any: Value returned by ``GoogleSpeechToTextLoader.load``. |
| `load_google_bucket()` | `load_google_bucket( project_name: str, bucket: str, prefix: Optional[str] = None, continue_on_failure: bool = False ) -> Any` | Load source content. Provides direct module-level access to ``GoogleBucketLoader.load`` using a fresh ``GoogleBucketLoader`` instance. Any: Value returned by ``GoogleBucketLoader.load``. |
| `load_aws_bucket()` | `load_aws_bucket( bucket: str, prefix: Optional[str] = None, aws_access_key_id: Optional[str] = None, aws_secret_access_key: Optional[str] = None, aws_session_token: Optional[str] = None, region_name: Optional[str] = None, endpoint_url: Optional[str] = None ) -> Any` | Load source content. Provides direct module-level access to ``AwsBucketLoader.load`` using a fresh ``AwsBucketLoader`` instance. Any: Value returned by ``AwsBucketLoader.load``. |

## How to choose

Use the functional wrapper when one call completes the task. Use the implementation class when you need retained state, helper methods, or direct provider debugging.

## Operational considerations

- Cloud SDK credentials are commonly required.
- Authentication failures and missing Python dependencies are separate problems.
- Large objects may be expensive in memory and network transfer.

## Representative Functions

### `load_google_drive_file()`

```python
# load_google_drive_file( file_id: str, recursive: bool = False ) -> Any
```

Load a provider file. Provides direct module-level access to ``GoogleDriveLoader.load_file`` using a fresh ``GoogleDriveLoader`` instance. Any: Value returned by ``GoogleDriveLoader.load_file``.

### `load_google_drive_folder()`

```python
# load_google_drive_folder( folder_id: str, recursive: bool = False ) -> Any
```

Load provider folder content. Provides direct module-level access to ``GoogleDriveLoader.load_folder`` using a fresh ``GoogleDriveLoader`` instance. Any: Value returned by ``GoogleDriveLoader.load_folder``.

### `load_onedrive()`

```python
# load_onedrive( drive_id: str, folder_path: Optional[str] = None, object_ids: Optional[List[str]] = None, auth_with_token: bool = True ) -> Any
```

Load source content. Provides direct module-level access to ``OneDriveDocLoader.load`` using a fresh ``OneDriveDocLoader`` instance. Any: Value returned by ``OneDriveDocLoader.load``.

### `load_google_cloud_file()`

```python
# load_google_cloud_file( project_name: str, bucket: str, blob: str ) -> Any
```

Load source content. Provides direct module-level access to ``GoogleCloudFileLoader.load`` using a fresh ``GoogleCloudFileLoader`` instance. Any: Value returned by ``GoogleCloudFileLoader.load``.

### `load_aws_file()`

```python
# load_aws_file( bucket: str, key: str, aws_access_key_id: Optional[str] = None, aws_secret_access_key: Optional[str] = None, aws_session_token: Optional[str] = None, region_name: Optional[str] = None ) -> Any
```

Load source content. Provides direct module-level access to ``AwsFileLoader.load`` using a fresh ``AwsFileLoader`` instance. Any: Value returned by ``AwsFileLoader.load``.

### `load_google_speech_to_text()`

```python
# load_google_speech_to_text( project_id: str, file_path: str, config: Optional[Dict[str, Any]] = None ) -> Any
```

Load source content. Provides direct module-level access to ``GoogleSpeechToTextLoader.load`` using a fresh ``GoogleSpeechToTextLoader`` instance. Any: Value returned by ``GoogleSpeechToTextLoader.load``.

### `load_google_bucket()`

```python
# load_google_bucket( project_name: str, bucket: str, prefix: Optional[str] = None, continue_on_failure: bool = False ) -> Any
```

Load source content. Provides direct module-level access to ``GoogleBucketLoader.load`` using a fresh ``GoogleBucketLoader`` instance. Any: Value returned by ``GoogleBucketLoader.load``.

### `load_aws_bucket()`

```python
# load_aws_bucket( bucket: str, prefix: Optional[str] = None, aws_access_key_id: Optional[str] = None, aws_secret_access_key: Optional[str] = None, aws_session_token: Optional[str] = None, region_name: Optional[str] = None, endpoint_url: Optional[str] = None ) -> Any
```

Load source content. Provides direct module-level access to ``AwsBucketLoader.load`` using a fresh ``AwsBucketLoader`` instance. Any: Value returned by ``AwsBucketLoader.load``.


See [Functional API](../api/fonky.md) for all signatures.

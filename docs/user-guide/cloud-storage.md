# Cloud & Storage

**Tools:** 8

Examples use the Google ADK callable wrapper surface so each example is directly executable as ordinary Python.

## Tool Index

| Tool |
|---|
| [`load_google_drive_file`](#load_google_drive_file) |
| [`load_google_drive_folder`](#load_google_drive_folder) |
| [`load_onedrive`](#load_onedrive) |
| [`load_google_cloud_file`](#load_google_cloud_file) |
| [`load_aws_file`](#load_aws_file) |
| [`load_google_speech_to_text`](#load_google_speech_to_text) |
| [`load_google_bucket`](#load_google_bucket) |
| [`load_aws_bucket`](#load_aws_bucket) |

---

## `load_google_drive_file`

Load a Google Drive file.

### Signature

```python
def load_google_drive_file( file_id: str, recursive: bool=False ) -> Any
```

### Purpose

Load a Google Drive file using the Google Drive loader. Boolean options control retrieval depth or supplemental content.

### Example

```python
from fonky.gemini.tools import load_google_drive_file

result = load_google_drive_file(
    file_id='file-id' )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `file_id` | `str` | Provider file identifier used to load a single file. |
| `recursive` | `bool` | Whether the loader should traverse nested provider or URL resources. |

### Returns

Any: LangChain documents loaded from the requested source.

### Raises

Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the project error type.

---

## `load_google_drive_folder`

Load documents from a Google Drive folder.

### Signature

```python
def load_google_drive_folder( folder_id: str, recursive: bool=False ) -> Any
```

### Purpose

Load documents from a Google Drive folder using the Google Drive loader. Boolean options control retrieval depth or supplemental content.

### Example

```python
from fonky.gemini.tools import load_google_drive_folder

result = load_google_drive_folder(
    folder_id='folder-id' )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `folder_id` | `str` | Provider folder identifier used to load folder contents. |
| `recursive` | `bool` | Whether the loader should traverse nested provider or URL resources. |

### Returns

Any: LangChain documents loaded from the requested source.

### Raises

Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the project error type.

---

## `load_onedrive`

Load documents from OneDrive.

### Signature

```python
def load_onedrive( drive_id: str, folder_path: Optional[str]=None, object_ids: Optional[List[str]]=None, auth_with_token: bool=True ) -> Any
```

### Purpose

Load documents from OneDrive using the OneDrive loader.

### Example

```python
from fonky.gemini.tools import load_onedrive

result = load_onedrive(
    drive_id='drive-id' )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `drive_id` | `str` | OneDrive drive identifier. |
| `folder_path` | `Optional[str]` | Optional folder path within the selected drive. |
| `object_ids` | `Optional[List[str]]` | Optional provider object identifiers to load. |
| `auth_with_token` | `bool` | Whether token-based authentication should be used. |

### Returns

Any: LangChain documents loaded from the requested source.

### Raises

Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the project error type.

---

## `load_google_cloud_file`

Load a Google Cloud Storage object.

### Signature

```python
def load_google_cloud_file( project_name: str, bucket: str, blob: str ) -> Any
```

### Purpose

Load a Google Cloud Storage object using the Google Cloud Storage loader.

### Example

```python
from fonky.gemini.tools import load_google_cloud_file

result = load_google_cloud_file(
    project_name='example-project',
    bucket='example-bucket',
    blob='documents/report.pdf' )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `project_name` | `str` | Google Cloud project name used by the storage loader. |
| `bucket` | `str` | Storage bucket name. |
| `blob` | `str` | Cloud storage object name. |

### Returns

Any: LangChain documents loaded from the requested source.

### Raises

Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the project error type.

---

## `load_aws_file`

Load an Amazon S3 object.

### Signature

```python
def load_aws_file( bucket: str, key: str, aws_access_key_id: Optional[str]=None, aws_secret_access_key: Optional[str]=None, aws_session_token: Optional[str]=None, region_name: Optional[str]=None ) -> Any
```

### Purpose

Load an Amazon S3 object using the Amazon S3 file loader.

### Example

```python
from fonky.gemini.tools import load_aws_file

result = load_aws_file(
    bucket='example-bucket',
    key='documents/report.pdf' )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `bucket` | `str` | Storage bucket name. |
| `key` | `str` | Amazon S3 object key. |
| `aws_access_key_id` | `Optional[str]` | Provider identifier for the selected aws access key. |
| `aws_secret_access_key` | `Optional[str]` | AWS credential or configuration value for secret access key. |
| `aws_session_token` | `Optional[str]` | AWS credential or configuration value for session token. |
| `region_name` | `Optional[str]` | Cloud region name used to configure the storage client. |

### Returns

Any: LangChain documents loaded from the requested source.

### Raises

Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the project error type.

---

## `load_google_speech_to_text`

Transcribe audio with Google Speech-to-Text.

### Signature

```python
def load_google_speech_to_text( project_id: str, file_path: str, config: Optional[Dict[str, Any]]=None ) -> Any
```

### Purpose

Transcribe audio with Google Speech-to-Text using the Google Speech-to-Text loader.

### Example

```python
from fonky.gemini.tools import load_google_speech_to_text

result = load_google_speech_to_text(
    project_id='example-project',
    file_path='data/audio.wav' )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `project_id` | `str` | Google Cloud project identifier used by the speech loader. |
| `file_path` | `str` | Local filesystem path to the source file. |
| `config` | `Optional[Dict[str, Any]]` | Optional provider configuration mapping. |

### Returns

Any: LangChain documents loaded from the requested source.

### Raises

Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the project error type. the project error type.

---

## `load_google_bucket`

Load documents from a Google Cloud Storage bucket.

### Signature

```python
def load_google_bucket( project_name: str, bucket: str, prefix: Optional[str]=None, continue_on_failure: bool=False ) -> Any
```

### Purpose

Load documents from a Google Cloud Storage bucket using the Google Cloud Storage bucket loader.

### Example

```python
from fonky.gemini.tools import load_google_bucket

result = load_google_bucket(
    project_name='example-project',
    bucket='example-bucket' )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `project_name` | `str` | Google Cloud project name used by the storage loader. |
| `bucket` | `str` | Storage bucket name. |
| `prefix` | `Optional[str]` | Optional object-name prefix used to restrict cloud storage results. |
| `continue_on_failure` | `bool` | Whether loading should continue when an individual object fails. |

### Returns

Any: LangChain documents loaded from the requested source.

### Raises

Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the project error type.

---

## `load_aws_bucket`

Load documents from an Amazon S3 bucket.

### Signature

```python
def load_aws_bucket( bucket: str, prefix: Optional[str]=None, aws_access_key_id: Optional[str]=None, aws_secret_access_key: Optional[str]=None, aws_session_token: Optional[str]=None, region_name: Optional[str]=None, endpoint_url: Optional[str]=None ) -> Any
```

### Purpose

Load documents from an Amazon S3 bucket using the Amazon S3 bucket loader.

### Example

```python
from fonky.gemini.tools import load_aws_bucket

result = load_aws_bucket(
    bucket='example-bucket' )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `bucket` | `str` | Storage bucket name. |
| `prefix` | `Optional[str]` | Optional object-name prefix used to restrict cloud storage results. |
| `aws_access_key_id` | `Optional[str]` | Provider identifier for the selected aws access key. |
| `aws_secret_access_key` | `Optional[str]` | AWS credential or configuration value for secret access key. |
| `aws_session_token` | `Optional[str]` | AWS credential or configuration value for session token. |
| `region_name` | `Optional[str]` | Cloud region name used to configure the storage client. |
| `endpoint_url` | `Optional[str]` | Optional alternate service endpoint URL. |

### Returns

Any: LangChain documents loaded from the requested source.

### Raises

Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the project error type.

---

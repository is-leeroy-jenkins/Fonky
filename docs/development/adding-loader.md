# Adding a Loader

A loader owns source validation, integration loader construction, document loading, metadata shaping, optional splitting/chunking, and loader-specific failures. Retain state only when later operations genuinely depend on earlier ones.

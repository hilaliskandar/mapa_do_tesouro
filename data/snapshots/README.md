# Canonical source snapshots

Canonical data snapshots used for rebuilds may live outside the public repository.

Each snapshot used by CI must have a public, versioned manifest in this directory with:

- logical snapshot id;
- universe id;
- data version;
- object key relative to the private R2 bucket;
- SHA-256;
- source period;
- expected municipality count;
- expected row count;
- semantic scope and exclusions.

Bucket names, account identifiers and credentials are operational configuration and are never committed.

A snapshot is accepted only after SHA-256 verification. An object present in R2 without a matching versioned manifest is not a canonical build input.

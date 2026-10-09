from __future__ import annotations

from pipeline.ingest.import_universe_catalog import (
    import_universe_catalog,
    read_universe_catalog,
)

read_territorial_catalog = read_universe_catalog
import_territorial_universes = import_universe_catalog


if __name__ == "__main__":
    from pipeline.ingest.import_universe_catalog import main

    main()

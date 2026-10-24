# Upstream

This launcher is a fork of **Free My TV (for LG webOS)** by Daniel Moreira and contributors.

- Repository: https://github.com/danielthejoker18/FreeMyTvWebOS
- Forked from commit: `76262eae5824352ddf4f77bf2db1c2e51a9e281b` (2026-10-23, v1.2.4)
- License: MIT — original notice kept in [`LICENSE`](LICENSE)

## Changes in TV Livre

| Change | Why |
|---|---|
| App id `io.github.fernandofasolo.tvlivre`, title "TV Livre" | Installs side by side with upstream, no name collision |
| Removed IP geolocation (`ipapi.co`) | Privacy: it sent the user's public IP to a third party. Without a city configured, weather falls back to São Paulo |
| Build packaging labels renamed | Branding only |

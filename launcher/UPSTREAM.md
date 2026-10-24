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
| **v0.2** Interface in Brazilian Portuguese, `pt-BR` dates | Target audience |
| **v0.2** Brazilian default catalog (Netflix, Prime, Disney+, YouTube, Globoplay, inputs); removed Plex/Crunchyroll/Homebrew defaults | Relevance; Homebrew needs root |
| **v0.2** App selector lists only apps installed on the TV | Less clutter |
| **v0.2** "Where to watch": TMDB trending (`pt-BR`) + watch providers for region `BR`, titles on the user's own apps first; card opens the right app | Main new feature |
| **v0.2** Without a TMDB key: shortcut cards to each service instead of hard-coded (and partly wrong) picks | Honesty |
| **v0.2** Own identity: green accent `#1fc77e`, new icon/splash (`scripts/make_assets.py`) | Branding |

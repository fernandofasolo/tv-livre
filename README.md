# TV Livre

**Kit aberto para deixar sua Smart TV LG mais rápida, sem anúncios e com mais privacidade.**
**Open kit to make your LG Smart TV faster, ad-free and more private.**

[🇧🇷 Português](#-português) · [🇺🇸 English](#-english)

> ⚠️ Projeto independente, sem afiliação com a LG Electronics. "LG" e "webOS" são marcas de seus respectivos donos. Use por sua conta e risco.
> Independent project, not affiliated with LG Electronics. "LG" and "webOS" are trademarks of their respective owners. Use at your own risk.

---

## 🇧🇷 Português

### O que tem aqui

| Pasta | O que é | Precisa de root? |
|---|---|---|
| [`docs/`](docs/guia.md) | Guia passo a passo: ajustes de privacidade, bloqueio por DNS, Modo Desenvolvedor, apps extras | Não |
| [`blocklist/`](blocklist/) | Listas de DNS para AdGuard Home / Pi-hole / NextDNS, em 3 níveis | Não |
| [`tools/`](tools/tvlivre.py) | CLI: achar a TV, parear, instalar `.ipk`, **renovar o Modo Desenvolvedor automaticamente** | Não |
| [`launcher/`](launcher/) | Home alternativa leve, sem anúncios (fork do [Free My TV](https://github.com/danielthejoker18/FreeMyTvWebOS)) | Não |

### Começo rápido

1. Siga o [guia](docs/guia.md) a partir da **Etapa 1** (ajustes sem risco).
2. Adicione as listas de bloqueio ao seu DNS (Etapa 2):
   - `https://raw.githubusercontent.com/fernandofasolo/tv-livre/main/blocklist/lg-ads.txt`
   - `https://raw.githubusercontent.com/fernandofasolo/tv-livre/main/blocklist/lg-tracking.txt`
3. Ative o Modo Desenvolvedor e instale o launcher (Etapa 3):

```bash
pip install cryptography
python tools/tvlivre.py discover
python tools/tvlivre.py pair --ip 192.168.0.50
python launcher/scripts/build.py
python tools/tvlivre.py install launcher/dist/io.github.fernandofasolo.tvlivre_0.1.0_all.ipk
python tools/tvlivre.py schedule-renew      # Windows: renova o Dev Mode toda segunda
```

Ou baixe o `.ipk` pronto na página de [Releases](../../releases). Ele é gerado pelo GitHub Actions a partir deste código e vem com o hash SHA-256.

### Status

`v0.1`: em construção.

| Modelo testado | webOS | Firmware | `pair` | `install` | `devmode-status` / `renew` | Root |
|---|---|---|---|---|---|---|
| 55UQ8050PSB | 22 | 04.60.90 | ✅ | ✅ | ✅ | ❌ firmware corrigido |

As listas de bloqueio e a renovação do Dev Mode precisam de validação em mais modelos. Abra uma issue com o modelo da TV, a versão do webOS e o que funcionou ou quebrou.

---

## 🇺🇸 English

### What's inside

| Folder | What it is | Root needed? |
|---|---|---|
| [`docs/`](docs/guia.md) | Step-by-step guide (Portuguese first, English summary below) | No |
| [`blocklist/`](blocklist/) | DNS blocklists for AdGuard Home / Pi-hole / NextDNS, in 3 tiers | No |
| [`tools/`](tools/tvlivre.py) | CLI: discover the TV, pair, install `.ipk`, **auto-renew Developer Mode** | No |
| [`launcher/`](launcher/) | Lightweight ad-free home screen (fork of [Free My TV](https://github.com/danielthejoker18/FreeMyTvWebOS)) | No |

### Quick start

1. **Privacy settings:** turn off *Live Plus* (ACR) and decline the optional ad/viewing-data agreements.
2. **DNS blocking:** add `blocklist/lg-ads.txt` and `blocklist/lg-tracking.txt` to AdGuard Home or Pi-hole. `lg-aggressive.txt` blocks the LG store and updates; it's opt-in.
3. **Developer Mode + launcher:** run the commands in the Portuguese section above. `schedule-renew` creates a weekly Windows task, so the 1000-hour Dev Mode session never expires and wipes your apps.

### Blocklist tiers

| File | Blocks | Breaks |
|---|---|---|
| `lg-ads.txt` | LG ad servers | Nothing expected |
| `lg-tracking.txt` | Telemetry, ACR | LG ThinQ phone control |
| `lg-aggressive.txt` | Store/platform/firmware update domains | Content Store, app & firmware updates |

---

## Créditos / Credits

- Launcher baseado em / based on [danielthejoker18/FreeMyTvWebOS](https://github.com/danielthejoker18/FreeMyTvWebOS) (MIT). Veja / see [`launcher/UPSTREAM.md`](launcher/UPSTREAM.md).
- Comunidade / community: [webosbrew.org](https://www.webosbrew.org/), [lg-tv-ad-block](https://github.com/hugobatista/lg-tv-ad-block/).
- Clima / weather: [Open-Meteo](https://open-meteo.com/) · Filmes / movies: [TMDB](https://www.themoviedb.org/), [TVMaze](https://www.tvmaze.com/).

## Licença / License

[MIT](LICENSE). O launcher mantém também o aviso de copyright original em [`launcher/LICENSE`](launcher/LICENSE).

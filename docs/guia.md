# Guia TV Livre

Siga as etapas em ordem. Cada uma funciona sozinha. Se parar na Etapa 2, já terá ganhado muito.

## Etapa 0 — Conheça sua TV

Em **Configurações → Geral → Sobre esta TV**, anote:

- Modelo (ex.: `OLED55C3PSA`)
- Versão do webOS e do firmware (ex.: `webOS 23 / 33.22.65`)

> ⚠️ Se você pensa em fazer root no futuro, **desligue a atualização automática de software** agora
> (Configurações → Suporte → Atualização de software). A LG corrige as falhas usadas para root
> nas atualizações. Veja https://www.webosbrew.org/rooting/

## Etapa 1 — Ajustes sem risco (~15 min)

Os nomes dos menus variam por versão do webOS.

- [ ] **Live Plus** (reconhecimento de conteúdo / ACR): **desligar**. Fica em Geral → Sistema → Configurações adicionais.
- [ ] **Contratos de usuário**: recusar os opcionais (publicidade personalizada, informações de visualização, recomendações). Fica em Geral → Sistema → Contratos do usuário.
- [ ] **Publicidade/recomendação na Home**: desligar "Home Promotion", "Recomendações de conteúdo" e "Reprodução automática na Home".
- [ ] **Apps pré-instalados** que você não usa: desinstalar.
- [ ] **Notificações** promocionais: desligar.
- [ ] **Quick Start+**: ligado = liga mais rápido; desligado = cada boot limpa a memória. Teste os dois.
- [ ] **Rede**: use cabo se puder e reserve um IP fixo para a TV no roteador (necessário para as próximas etapas).

## Etapa 2 — Bloqueio por DNS

Bloqueie anúncios e rastreamento na sua rede, sem mexer na TV.

1. Tenha um DNS bloqueador: **AdGuard Home** ou **Pi-hole v6+** (Raspberry Pi, NAS, Docker) ou **NextDNS**.
2. Adicione as listas (em AdGuard Home: Filtros → Listas de bloqueio DNS → Adicionar lista):
   - Anúncios: `https://raw.githubusercontent.com/fernandofasolo/tv-livre/main/blocklist/lg-ads.txt`
   - Rastreamento: `https://raw.githubusercontent.com/fernandofasolo/tv-livre/main/blocklist/lg-tracking.txt`
3. Aponte o DNS da TV (ou da rede toda, no DHCP do roteador) para esse servidor.
4. Use a TV por 1–2 dias e confira o **log de consultas**. Se algo quebrar, libere o domínio e [abra uma issue](../../../issues).

`lg-aggressive.txt` bloqueia a loja e as atualizações da LG. Só use se souber por que quer isso.

## Etapa 3 — Modo Desenvolvedor + launcher

1. Crie uma conta gratuita em https://webostv.developer.lge.com
2. Na TV, instale o app **Developer Mode** pela LG Content Store, entre com a conta e ligue **Dev Mode Status**. A TV reinicia.
3. Abra o Developer Mode de novo, ligue **Key Server** e anote o **IP** e a **Passphrase**.
4. No PC (Python 3.9+):

```bash
pip install cryptography
python tools/tvlivre.py pair --ip <IP> --passphrase <PASSPHRASE>
python launcher/scripts/build.py
python tools/tvlivre.py install launcher/dist/io.github.fernandofasolo.tvlivre_<versão>_all.ipk
```

5. No launcher, abra **⚙️ Personalizar**:
   - Escreva sua **cidade** (para o clima).
   - Escolha até 8 apps.
   - Nomeie as portas HDMI.
   - Se a TV for OLED, use o tema **Preto total**.
   - **Onde assistir:** crie uma conta grátis em https://www.themoviedb.org, gere a chave em *Configurações → API* e cole em **Chave da API do TMDB**. A fileira "Em alta" passa a mostrar os filmes e séries da semana, **em qual streaming estão no Brasil**, priorizando os que você assina. O OK abre o app certo.
6. Atalho: dentro do launcher, **segure o botão `1`** do controle e associe o TV Livre a ele.

### Não deixe o Modo Desenvolvedor expirar

A sessão dura **1000 horas (~41 dias)**. Quando ela expira, **a TV apaga os apps instalados**.

```bash
python tools/tvlivre.py devmode-status    # quanto tempo falta
python tools/tvlivre.py devmode-renew     # renova agora
python tools/tvlivre.py schedule-renew    # Windows: renova toda segunda às 09:00
```

O PC precisa estar ligado e na mesma rede da TV no horário agendado. Toda segunda já é bem mais frequente que o necessário.

## Etapa 4 — Apps extras (Modo Desenvolvedor ou Homebrew Channel)

| App | O que faz |
|---|---|
| [YouTube AdFree](https://repo.webosbrew.org/apps/youtube.leanback.v4) | YouTube sem anúncios + SponsorBlock |
| Moonlight | Jogar os games do PC na TV |
| Jellyfin / Kodi | Sua biblioteca de mídia |
| [PicCap](https://repo.webosbrew.org/apps/org.webosbrew.piccap/) | Ambilight com fita de LED (**exige root**) |

Instale com `python tools/tvlivre.py install <arquivo.ipk>` ou pelo [webOS Dev Manager](https://github.com/webosbrew/dev-manager-desktop).

## Etapa 5 — Root (opcional, avançado)

Fora do escopo deste repositório. Siga **apenas** a documentação oficial da comunidade: https://www.webosbrew.org/rooting/
Com root você ganha: fim da expiração do Dev Mode, remapear o botão Home e bloquear domínios na própria TV.

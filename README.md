# news-image-20261121

[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/blupoint44/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/blupoint44/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

## The World in One Day, Saturday 21 November 2026

A program that draws one newspaper front page summing up the world news of
**Saturday 21 November 2026** in a single 1024×1024 PNG image.

`main.py` is pure Python 3.13 standard library, with no network access. It
renders the page deterministically with its own raster canvas, its own 5×7
bitmap font and its own zlib PNG encoder — run it twice and you get identical
bytes.

## The day's headlines (21 November 2026)

Lead story:

- **Russian missile hits Poland as Kyiv bridges struck** — Polish PM Donald
  Tusk called the missile that landed in Poland a likely deliberate
  provocation, as a mass Russian strike hit three Kyiv bridges and Kryvyi
  Rih, killing 2 and injuring 42, four of them children. (AP, BBC, Reuters
  reporting via news aggregators, 21 Nov 2026)

Panels:

- **UK and EU strike landmark deal to rebuild ties** — food exports,
  emissions trading and a youth experience scheme agreed; PM Burnham said the
  UK would explore even closer ties. (BBC, 21 Nov 2026)
- **Trump, Xi and Putin issue joint peace declaration** — joint declaration
  on peace and security after the Shenzhen trilateral summit; envoy Kushner
  said Russia was "comfortable" with NATO-like security guarantees for
  Ukraine. (AP, 21 Nov 2026)
- **Myanmar genocide verdict: Rohingya rejoice** — Rohingya refugees in
  Bangladesh welcomed the International Court of Justice ruling holding
  Myanmar responsible for genocide; the UK expelled Myanmar's diplomat.
  (AP, BBC, 21 Nov 2026)
- **Tech sell-off deepens as Anthropic shares slide** — AI stocks dragged
  markets down after Anthropic's record IPO; Asian shares headed for their
  worst week since 2020. (BBC, Reuters, 21 Nov 2026)
- **Denmark foils alleged Russian assassination plot** — Denmark expelled a
  Russian diplomat over an alleged plot to kill a US-Ukrainian rapper.
  (Al Jazeera, BBC, 21 Nov 2026)
- **Anthropic AI may have solved the Riemann hypothesis** — in a year of AI
  solving maths problems, Anthropic may have just solved the biggest.
  (BBC, 21 Nov 2026)

Also today:

- Tanker ablaze in the Strait of Hormuz after a projectile hit near Oman (UKMTO)
- Trump threatens a ban on US firms building AI data centres overseas (BBC)
- Mamdani unveils a plan to close New York's Rikers Island jail by 2032 (BBC, AP)

## Guide

- Bounty page: https://make.fun/bounty/news-image-20261121 — "Sum up
  21 November's world news in one image", $100 in USDC, top 50 paid, entries
  close 2026-11-23T00:00:00Z.
- Your program must write `/output/entry.png` (or
  `$MAKEFUN_OUTPUT_DIR/entry.png`), at most 1024×1024 pixels and 1 MiB, with
  no network, and produce identical bytes on both runs.
- Join make.fun and enter your own agent's work:
  https://make.fun/?ref=cc9ads3n

## License

MIT — see `LICENSE`.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
# writes out/entry.png (1024x1024 PNG, under 1 MiB, deterministic)
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=cc9ads3n&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121) · AI agents build software for cash rewards</sub>

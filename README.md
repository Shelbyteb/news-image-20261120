# The World in One Day — 20 November 2026

[![news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/Shelbyteb/news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/Shelbyteb/news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120)

A newspaper front page summing up the world's news of Friday 20 November
2026, built for the [news-image-20261120 bounty on make.fun](https://make.fun/bounty/news-image-20261120).

Lead story: Severe Cyclonic Storm Akvan makes landfall on India's east
coast at midday, with more than 300,000 people evacuated. Also on the
page: the COP31 final plenary in Antalya closes without a fossil-fuel
pledge; Russian strikes damage the Austrian and Dutch embassies in Kyiv;
Trump, Xi and Putin hold their first three-way talks at APEC in Shenzhen;
Fiji declares a disaster as drought bites; and South Korea's Supreme
Court clears former prime minister Han Duck-soo.

## Files

- `entry.png` — the front-page image (1024×1024, drawn by
  `make_frontpage.py` with Pillow).
- `make_frontpage.py` — the drawing script; run it to regenerate the image.
- `main.ts` — the entrypoint: copies `entry.png` to the output folder.

## Run

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

## License

MIT — see `LICENSE`.

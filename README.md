# The World in One Day — 20 November 2026

[![news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/Shelbyteb/news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/Shelbyteb/news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120)

A newspaper front page summing up the world's news of Friday 20 November
2026, built for the [news-image-20261120 bounty on make.fun](https://make.fun/bounty/news-image-20261120).

Lead story: President Trump says there is "no rush" on a decision over
war with Iran and pushes it into 2027. Also on the page: Cyclone Akvan
bears down on Odisha with 300,000 people evacuated; NASA confirms
Voyager 1 is now a full light-day from Earth; Europe says it is open to
talks with Russia on ending the Ukraine war; the UN's top court rules
Myanmar committed genocide against the Rohingya; engine trouble ends
Japan's Hayabusa2 asteroid landing plan; plus briefs on GTA 6 sales,
New Zealand's Test against India, and a migrant boat sinking off
Senegal.

## Files

- `entry.png` — the front-page image (1024×1024, drawn by
  `draw_frontpage.py` with Pillow; no photograph or clip art is used).
- `draw_frontpage.py` — the drawing script; run it to regenerate the
  image from scratch.
- `main.ts` — the entrypoint (Node 22, standard library only): copies
  `entry.png` to the output folder.

## Run

```sh
python3 draw_frontpage.py
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

## License

MIT — see `LICENSE`.

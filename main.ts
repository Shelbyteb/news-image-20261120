// Entry for the news-image-20261120 bounty on make.fun.
//
// The front page for Friday 20 November 2026 is the entry.png next to
// this file, drawn by draw_frontpage.py with Pillow. This program runs
// with Node 22 and the standard library only: it reads that image and
// writes the same bytes to the grader's output folder, so both runs of
// the program produce an identical file.
//
// Outside the grader, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';

mkdirSync(outDir, { recursive: true });
const image = readFileSync(join(here, 'entry.png'));
writeFileSync(join(outDir, 'entry.png'), image);

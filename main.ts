// News-image entry for 20 November 2026 (Node 22, standard library only).
// The front page is the entry.png beside this file, drawn by
// make_frontpage.py; this program copies it to the grader's output folder.
//
// Run it outside the grader with:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync } from 'node:fs';
import { join } from 'node:path';

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
copyFileSync(new URL('./entry.png', import.meta.url),
             join(outDir, 'entry.png'));

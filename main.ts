// gta6-meme-x-01 entry (Node 22, standard library only): copies POST.json from
// the repository root to /output/POST.json, where the gate reads it. The entry
// is the X post itself: the house reads the post from X (its first picture and
// its text) and hands that to the judge. Nothing this program writes is judged.
//
// POST.json holds a placeholder until the meme is posted from @jonastama7;
// replace it with the post's address before submitting.
//
// Outside the grader's container, MAKEFUN_BOT_DIR and MAKEFUN_OUTPUT_DIR stand
// in for /bot and /output:
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, existsSync, mkdirSync, readFileSync, statSync } from 'node:fs';
import { join } from 'node:path';

const BOT_DIR = process.env.MAKEFUN_BOT_DIR ?? '/bot';
const OUTPUT_DIR = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';

mkdirSync(OUTPUT_DIR, { recursive: true });

const postPath = join(BOT_DIR, 'POST.json');
const raw = readFileSync(postPath, 'utf8');
const post = JSON.parse(raw) as { url?: unknown };
if (typeof post.url !== 'string' || post.url.length === 0) {
  console.error('POST.json has no url string');
  process.exit(1);
}

// The post's first picture is the meme that gets judged: it must be in the
// repo next to POST.json, and the url must be a real X post address before
// submitting. Neither failure stops the copy (the gate judges them), but both
// are reported here so a bad state is visible before submit.
const memePath = join(BOT_DIR, 'meme.jpg');
if (!existsSync(memePath)) {
  console.error('WARNING: meme.jpg is missing from the repository root');
} else {
  console.log(`meme.jpg present (${statSync(memePath).size} bytes)`);
}
if (!/^https?:\/\/(www\.|mobile\.)?(x\.com|twitter\.com)\/\S+\/status\/\d+/.test(post.url)) {
  console.error(`WARNING: url is not a real X post address yet: ${post.url}`);
}

copyFileSync(postPath, join(OUTPUT_DIR, 'POST.json'));
console.log(`POST.json copied to ${OUTPUT_DIR} (url: ${post.url})`);

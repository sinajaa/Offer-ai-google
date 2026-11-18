You are building an entry for the make.fun bounty "gta6-01" (Make GTA 6).

Work ONLY inside the current directory. It is a git repo laid out as an entrant's repository:
main.ts, serve.ts, vendor/makefun-game.ts (never modify), game/ (the game, static files),
screenshots/, shots.json, LICENSE, .makefun/owner.json.

GOAL: replace the starter's tiny 2D game in game/ with the most complete, highest-quality
ORIGINAL open-world crime game you can build. Original IP only: your own city name, characters,
vehicles, story, art, sound. Never use any name, logo, character, map, music or asset from
Grand Theft Auto or any other commercial game. Invent everything.

MUST HAVE (all of these, and they must be visible in the screenshots):
1. A 3D city you can explore on foot and by car: streets, blocks, buildings, sidewalks, a park,
   a waterfront, landmarks.
2. Traffic: cars driving the roads in lanes, slowing and stopping at intersections.
3. Pedestrians walking on sidewalks.
4. Vehicles you can steal and drive: E to enter/exit, acceleration, braking, steering,
   drift, a chase camera.
5. A wanted level (0-5 stars) that rises when you commit crimes (hit cars or pedestrians,
   shoot, damage property) and police who respond: police cars that chase you, officers that
   shoot at you, and the level decaying when you escape.
6. Missions and a short story: at least 4 missions with objectives, on-screen dialogue text,
   a marker/route to the objective, and a cash reward per mission.
7. Combat on foot: a pistol with aiming, muzzle flash, hit detection, health, damage,
   death and respawn at a hospital.
8. A HUD: health bar, wanted stars, money, in-game clock, mission objective text, and a
   minimap (canvas-drawn: roads, player arrow, police blips, mission markers).
9. A start screen (title + Play), a pause menu, and save/load in localStorage (money,
   missions completed, position).
10. Polish: a camera that feels right, effects (muzzle flash, tire smoke, screen shake),
    synthesized sound with WebAudio (engine, gunshot, siren, footsteps), readable menus.

HARD TECHNICAL CONSTRAINTS:
- game/ is served as static files at a static server's root; game/index.html must open in
  desktop Chrome and play with NO network request. Every script, image, sound and font is a
  file under game/ or a data: URI.
- Vendor any library under game/vendor/ and only as a minified build named *.min.js or
  *.min.mjs. Use three.js: save the minified ESM build to game/vendor/three.module.min.js
  (e.g. curl -sSL https://unpkg.com/three@0.160.0/build/three.module.min.js -o that path)
  and map it in index.html with an import map: {"imports":{"three":"./vendor/three.module.min.js"}}.
- Limits: at most 993 files+directories under game/, 48 MiB total, game/index.html at most
  1 MiB. Every reference in index.html and in every reachable .js/.mjs must resolve to a file
  inside game/ or a data: URI: no http(s) URLs, no protocol-relative //host, no CDN, no
  bare specifier that the import map does not map.
- Split your own source into small ES modules under game/src/ with one clear job each, named
  for what they do: city.js, roads.js, traffic.js, pedestrians.js, player.js, vehicles.js,
  police.js, wanted.js, missions.js, combat.js, hud.js, minimap.js, audio.js, save.js,
  ui.js, shots.js, main.js. The judge sees file names and first declarations, so naming and
  structure matter.
- Controls: WASD move, mouse look, Shift sprint, E enter/exit vehicle, mouse click to shoot,
  Esc pause.

SCREENSHOTS (required, exactly 4 JPEGs, 1280x720):
- Implement deterministic screenshot scenes addressed as game/index.html?shot=<name>&seed=1
  with these names: street, car, chase, mission. Each must set up a real, live-looking frame:
  * street: on foot on a busy street, traffic and pedestrians around, HUD and minimap visible.
  * car: driving a stolen car through traffic, chase camera, speed HUD.
  * chase: 3-star wanted level, two police cars right behind, muzzle flash, minimap with blips.
  * mission: a mission objective active, marker visible, objective text on the HUD.
  Advance the simulation deterministically (fixed timestep from the seed) so the frame looks
  alive and the same seed always gives the same frame.
- Write scripts/shoot.mjs (Node, standard library plus sharp at
  /workspace/project/mf/tools/node_modules/sharp) that for each scene runs:
  chromium --headless=new --no-sandbox --disable-gpu --hide-scrollbars --window-size=1280,720
  --virtual-time-budget=6000 --screenshot=/tmp/<name>.png
  "file://<repo>/game/index.html?shot=<name>&seed=1"
  then converts with sharp: resize 1280x720 (fit: fill), jpeg quality 82, and writes
  screenshots/1-street.jpg, 2-car.jpg, 3-chase.jpg, 4-mission.jpg.
  Delete the starter's screenshots first. Each JPEG must be <= 250 KB and exactly 1280x720.

README.md at the repository root: write it with these badge lines exactly (owner sinajaa,
repo gta6-bot), then a short description of the game and how to run it:

# gta6-bot

[![make.fun · gta6-01](https://make.fun/badge/gta6-01.svg)](https://make.fun/bounty/gta6-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-01)
[![rank](https://make.fun/badge/gta6-01/sinajaa/gta6-bot/rank.svg)](https://make.fun/bounty/gta6-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=gta6-01)
[![reward](https://make.fun/badge/gta6-01/sinajaa/gta6-bot/reward.svg)](https://make.fun/bounty/gta6-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-01)

main.ts: edit it with lines you write (for example log a one-line summary of what was
written: file count, screenshot count, entry title). It must keep working:
`MAKEFUN_OUTPUT_DIR=out node main.ts` succeeds and writes out/game, out/screenshots,
out/dossier.json.

VERIFY BEFORE YOU FINISH:
1. rm -rf out && mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts  (exit 0, dossier written)
2. node scripts/shoot.mjs  (four JPEGs, each <= 250 KB, 1280x720)
3. No external references: grep -RIn "https\?://" game/index.html game/src || true
   (only data: URIs and local paths allowed in game/index.html and game/src)
4. Each scene renders without JS errors:
   chromium --headless=new --no-sandbox --disable-gpu --virtual-time-budget=4000
   --dump-dom "file://<repo>/game/index.html?shot=street&seed=1" | grep -io "<canvas" | head -1
   Repeat for car, chase, mission.

Work in small steps and keep the game playable at every step. When you are done, print a short
report: the systems you built, the file list under game/src, and any known gaps.

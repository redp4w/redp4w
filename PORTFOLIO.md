# redp4w profile integration

This profile is the landing page; [redp4w.github.io](https://redp4w.github.io/) hosts the full articles. The section between `<!-- LATEST:START -->` and `<!-- LATEST:END -->` is maintained by `.github/workflows/sync-latest.yml` every 6 hours and on manual dispatch. It reads the JSON published at `/latest.json` and updates README.md only when the records change.

Existing `assets/` icons and certificate cards are reused. TryHackMe's local SVG remains a dated snapshot, not a live metric. Hack The Box is left unlinked until an actual public profile is supplied.

Manual validation: `python3 -m unittest discover -s scripts -p 'test_*.py' -v`.

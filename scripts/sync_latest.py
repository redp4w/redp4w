#!/usr/bin/env python3
"""Update only the LATEST markers in the profile README from the published site JSON."""
import argparse
import html
import json
import re
import sys
from datetime import date
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import urlopen

START = '<!-- LATEST:START -->'
END = '<!-- LATEST:END -->'
FEED = 'https://redp4w.github.io/latest.json'


def render(feed: dict) -> str:
    posts = feed.get('posts')
    if not isinstance(posts, list) or not posts:
        raise ValueError('The published feed must contain at least one post.')
    rows = []
    for post in posts[:3]:
        url = str(post['url'])
        parsed = urlparse(url)
        if parsed.scheme != 'https' or parsed.hostname != 'redp4w.github.io' or parsed.username or parsed.password or parsed.port:
            raise ValueError('Post URL must use the public portfolio HTTPS host.')
        when = date.fromisoformat(str(post['date'])).strftime('%d.%m.%Y')
        title = html.escape(str(post['title']), quote=True)
        category = html.escape(str(post.get('category') or 'Notas'), quote=True)
        link = html.escape(url, quote=True)
        rows.append(f'<tr><td><code>{when}</code></td><td><a href="{link}"><strong>{title}</strong></a><br><sub>{category} · publicação no portfólio</sub></td></tr>')
    return '<table>\n' + '\n'.join(rows) + '\n</table>'


def update(readme: str, table: str) -> str:
    if readme.count(START) != 1 or readme.count(END) != 1 or readme.index(START) > readme.index(END):
        raise ValueError('README markers are missing, repeated, or out of order.')
    expression = re.escape(START) + r'.*?' + re.escape(END)
    return re.sub(expression, lambda _: START + '\n' + table + '\n' + END, readme, count=1, flags=re.DOTALL)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--feed', default=FEED, help='Published JSON endpoint or local JSON fixture')
    parser.add_argument('--readme', type=Path, default=Path(__file__).resolve().parents[1] / 'README.md')
    args = parser.parse_args()
    if args.feed.startswith('https://'):
        with urlopen(args.feed, timeout=20) as response:
            feed = json.load(response)
    else:
        feed = json.loads(Path(args.feed).read_text(encoding='utf-8'))
    old = args.readme.read_text(encoding='utf-8')
    new = update(old, render(feed))
    if old != new:
        args.readme.write_text(new, encoding='utf-8')
        print('Updated latest posts from published site.')
    else:
        print('Latest posts already up to date.')
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
        print(f'Cannot update README safely: {exc}', file=sys.stderr)
        sys.exit(1)

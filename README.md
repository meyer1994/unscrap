# Unscrap

[![build](https://github.com/meyer1994/unscrap/actions/workflows/build.yml/badge.svg)](https://github.com/meyer1994/unscrap/actions/workflows/build.yml)
[![standard-readme compliant](https://img.shields.io/badge/readme%20style-standard-brightgreen.svg?style=flat-square)](https://github.com/RichardLitt/standard-readme)

A terrible idea

## Table of Contents

- [About](#about)
- [Install](#install)
- [Usage](#usage)

## About

I once read a comment on [Reddit][1] of someone complaining about
[Facebook's ugly HTML][2] and suggesting that companies would stop to show HTML
and would start serving static PNG/JPG for their pages.

Well... Here it is (?)... Sort of.

This application runs an HTTP server where the page is rendered on the server
and only an screenshot of it is returned to the browser.

**Features:**

- Not scalable
- Does not work on most websites
- Very stupid

**Roadmap:**

- Make it more stupid
- Needs more NFTs

## Install

This project uses [fastapi][3] and [uvicorn][4] for server interactions. The
web pages are rendered using [playwright][5].

```sh
$ pip install -r requirements.txt
```

## Usage

To run a local version of this project, just execute:

```sh
$ uvicorn app:app --reload
```

Then access `localhost:8000/` on your browser and delight yourself with the
_future of the web_.

[1]: https://reddit.com/
[2]: https://web.archive.org/web/20220106000653/https://old.reddit.com/r/assholedesign/comments/anila7/facebook_splitting_the_word_sponsored_to_bypass/
[3]: https://fastapi.tiangolo.com/
[4]: https://www.uvicorn.org/
[5]: https://playwright.dev/

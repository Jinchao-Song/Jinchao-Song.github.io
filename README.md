# Jinchao Song — academic homepage

Public address: https://jinchao-song.github.io/

This is a static GitHub Pages website, with no build step or package installation.
The existing Lora/Inter typography, green/blue palette, research pages and figures
have been retained while updating the academic content.

## Preview locally

From this directory, run `python -m http.server 8765 --bind 127.0.0.1` and open
http://127.0.0.1:8765/. Serve over HTTP so the citation snapshot can load.

## Updating the site

- `index.html`: biography, research overview, publications,
  fellowships, service and news. Paired `data-en` / `data-zh` attributes provide
  translated interface text; official course and publication titles stay in English.
- `site.css`: styling and mobile breakpoints.
- `site.js`: accessible hash navigation, language selection, publication filter
  and citation snapshot display. Main content and links also work without JavaScript.
- `project-1.html` to `project-4.html`: existing research detail pages.
  `project-4.css` styles the building-stock overview, which summarizes the
  author-supplied Research Briefing (question, methods, findings, implications
  and the Gang Liu/Jinchao Song Behind the paper contribution). Full original
  article figures remain linked and uncropped; projection assumptions and
  local planning limitations are retained.
- `assets/Jinchao_Song_CV.pdf`: current downloadable CV; replace this file after
  updating the master CV.
- `data/publications.json`: a reference copy of the verified publication entries;
  the displayed list is in `index.html` and should be kept in sync with it.
- `data/metrics.json`: a dated **Google Scholar** snapshot from profile
  `GwY9nlEAAAAJ`. `update_stats.py` reads citations and h-index from the **All**
  column, checks the profile identity and atomically saves the result.
  The existing weekly GitHub Action commits this JSON file when it changes;
  it becomes active for this version once these changes are published to `main`.
  If Google returns a challenge, an HTTP error or an unexpected page, the script
  fails and retains the last verified values and their original date.
  The published website reads this JSON directly from the repository's `main`
  branch, with the deployed snapshot as a fallback. This avoids depending on a
  Pages rebuild: commits made with `GITHUB_TOKEN` do not trigger branch-based
  Pages builds ([GitHub documentation](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)).
- `heat-map.gif`, `traffic-status.gif` and `vehicle-emissions.mp4`: original
  animated research assets, retained. The video is muted and loops automatically.
- `assets/building-material-stocks-fig1.png` and `...-fig3.png`: unmodified
  figures from the author's Nature Cities paper, with linked captions on the project page.
- `assets/grc-industrial-ecology-2026.png`: the user's original GRC poster-session
  photo, shown under conferences in News & Media.
- `assets/the-sun-weight-of-the-world-2026.jpg`: the supplied print clipping,
  available in the expandable The Sun entry. The original photo orientation is preserved.
- Homepage links to `#press-coverage` and `#press-sun` open
  the News & Media panel directly at the relevant content.

## Content conventions

- The 2026 Nature Cities article is published; its companion Research Briefing
  is listed separately and is not counted as a second research article.
- The homepage includes two short, attributed excerpts from the Research Briefing
  comments supplied by the author: Wei Chen (From the editor) and Ruidong Chang
  (Expert opinion). Ellipses mark omitted text, and a source link accompanies the
  excerpts. These are comments on the study; no reviewer identity is inferred.
- Teaching and mentoring remain in the downloadable CV, rather than a website section.
- Research experience, education, academic service and fellowships/awards are
  retained in the CV and omitted from About at the author's request.
- The Sun entry denotes print coverage, with no unsupported front-page or issue-date claim.
- Institutional/lab news is labeled separately from independent media coverage.
- The UMich story is marked "Featured on UMich SEAS": verified in the Featured
  position on https://seas.umich.edu/news on 20 September 2026. This refers to
  the SEAS news page, not a university-wide award or the U-M central homepage.
- No unpublished hobby-photo or video placeholders are displayed; the original
  version remains available in Git history.

## Sources for the September 2026 update

Content is based on the user's master CV, their direct teaching/mentoring
clarifications, and the linked publisher, university and lab records.

- https://www.nature.com/articles/s44284-026-00510-3
- https://www.nature.com/articles/s44284-026-00509-w
- https://www.nature.com/articles/s44284-026-00510-3/figures/1
- https://www.nature.com/articles/s44284-026-00510-3/figures/3
- https://scholar.google.com/citations?user=GwY9nlEAAAAJ&hl=en
- https://doi.org/10.1021/acs.est.5c05684
- https://www.nature.com/articles/s41597-025-05618-0
- https://surf-lab.earth/f/new-pub
- https://surf-lab.earth/f/gordon-research-conference-2026
- https://seas.umich.edu/news/weighing-600-million-buildings-help-construct-more-efficient-future

GitHub Pages is already enabled on the original repository. Changes in a local
checkout are previews until committed and pushed to the configured publishing branch.

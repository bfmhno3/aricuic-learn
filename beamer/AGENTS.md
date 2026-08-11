# Agent Instructions

This project is a subdirectory of `aricuic-lean` for creating presentation slides.

## Project Overview

```bash
│  .gitignore
│  .latexmkrc
│  main.tex
│  refs.bib
│
├─contents
├─figs
└─settings
    format.tex
    packages.tex
```

- `main.tex`: Entry file. It only stitches the sections together.
- `refs.bib`: Bibliography database. Stores references in BibTeX format; use `\cite{key}` in the body. When used with biblatex, specify the path in format.tex with `\addbibresource{refs.bib}`.
- `contents/`: Chapter content. Create subdirectories by chapter for book/report classes, or by section for article classes.
- `figs/`: Image assets. Use with `\graphicspath`; then reference files directly by filename in the body.
- `settings/packages.tex`: Package imports.
- `settings/format.tex`: Format configuration, such as page layout, title styles, and fonts.
- `.latexmkrc`: latexmk build configuration.

## Build Environment

- Use `latexmk` for normal verification.
- Use XeLaTeX whenever the package option includes `zh`; the style file loads `xeCJK` and OS-specific CJK fonts for Chinese mode.
- English-only slides may use `en`, but XeLaTeX remains the safest default because the repository examples and CJK support are built around it.
- Keep the document class as `\documentclass{beamer}` and load the package as `\usepackage[<theme>,<language>]{collegeBeamer}`.

## Coding Style

### Writing Rules

- Inline formulas must use `\(...\)`, for example `\(f(x)\)`.
- Display formulas must use the `equation` environment. Use `equation*` when numbering is not needed.
- All units must use commands from the `siunitx` package. Use lowercase unit names instead of legacy siunitx commands, for example `\qty{5}{kg}`.
- When Chinese text is mixed with numbers or English words, add spaces before and after the number or English word, for example `我 18 岁了`.
- Do not add a space before or after a number or English word when that side touches punctuation.
- Use Chinese full-width punctuation for all punctuation marks.
- Do not add spaces between Chinese text and punctuation.

### Project File Rules

- Files in `contents/` must not use numeric prefixes. Use the chapter name or a shortened chapter name, in lowercase with words separated by `_`.
- Add packages only in `settings/packages.tex`. Package options are allowed when importing packages.
- Add user-defined styles only in `settings/format.tex`.
- Use `\input` to import content from `contents/` and `settings/` into `main.tex`.
- Do not add content, import packages, or modify styles directly in `main.tex`.
- Do not use indentation in `.tex` files.

### `collegebeamer.sty` template usage

#### Package Options

- Theme options select colors and assets only. Add or change a theme in `collegebeamer.sty` with one `\DeclareOption{<name>}{...}` block.
- Language options select template strings and font support:
  - `en`: English table-of-contents and Q&A text.
  - `zh`: Chinese strings plus `xeCJK`; requires XeLaTeX.
- Prefer lowercase option names for new themes. Existing `CQU` is an exception; do not copy that casing unless preserving compatibility.

#### Theme Asset Layout

Each theme should live in `src/<Theme>/` and provide:

- `color-logo.png` or `.pdf`: logo used on normal white slides.
- `trans-logo.png` or `.pdf`: transparent/white logo used on colored slides.
- `background.png` or `.pdf`: title-page background.

In the matching `\DeclareOption`, set exactly these values:

```tex
\renewcommand{\maincolorRGB}{R, G, B}
\renewcommand{\colorlogoPath}{src/<Theme>/color-logo.png}
\renewcommand{\translogoPath}{src/<Theme>/trans-logo.png}
\renewcommand{\backgroundPath}{src/<Theme>/background.png}
```

Do not hard-code asset paths elsewhere.

#### Slide Authoring

- Start from `pre.tex`; replace metadata, sections, and frames without changing the package wiring.
- Use `\maketitle` for the branded cover page. It automatically applies the selected background and hides the footline.
- Use `\section{...}` for major divisions. The template automatically inserts a section table-of-contents slide.
- Use `\subsection{...}` when a standalone subsection divider is desired; the template inserts it automatically.
- Use `\QApage` for the final Q&A slide.
- Use `\bibliographpage` only when bibliography tooling is configured and `\printbibliography` is available.

#### Template Macros

Use the built-in macros instead of ad-hoc color commands:

- `\bhref{url}{text}` for colored links.
- `\centerstate{...}` for centered statement slides.
- `\ctextbf`, `\ctextsl`, `\cemph`, `\ctexttt` for main-color emphasis.
- `\btextbf`, `\btextsl`, `\bemph`, `\btexttt` for airforce-blue emphasis.
- `\tbf{text}` for bracketed monospace tags.
- `\themecolor{colorbg}` only for special colored pages; call theme color changes in the preamble or inside a local group, then restore scope.
- `\footlinecolor{<color>}` only when a visible footer is needed; the default is intentionally transparent.

#### Frame Patterns

- Use `\begin{frame}{Title}` for normal slides.
- Use `\begin{frame}[fragile]{Title}` for `lstlisting`, verbatim text, or code examples.
- Use `block`, `exampleblock`, and `alertblock` for semantic callouts; their colors are already themed.
- Use `columns` for image/text layouts instead of manual spacing-heavy arrangements.
- Keep slide text short. Let the theme carry branding; do not add competing logos, colors, or navigation elements inside frames.

#### Code Blocks

- Use `lstlisting`; the package already defines and applies `mystyle`.
- Mark code frames as `[fragile]`.
- Set `language=TeX` or another supported language when it improves highlighting.
- Do not redefine `\lstset` globally unless changing the repository-wide code-block style deliberately.

#### Style File Rules

- Keep theme declarations together with existing `\DeclareOption` blocks.
- Preserve the package-level defaults before option processing: PolyU assets and English strings are the fallback.
- Do not duplicate Beamer template definitions in slide files. Change `collegebeamer.sty` when behavior is part of the theme.
- Scope temporary visual changes with `\begingroup ... \endgroup` as existing title, section, Q&A, and bibliography pages do.
- Avoid changing geometry; the theme forces a 16:9 canvas with `paperwidth=16cm,paperheight=9cm`.
- Do not re-enable Beamer navigation symbols.

## Git Rules

- Use atomic commits. Commit one logical change at a time instead of batching unrelated work.
- Write commit messages in Conventional Commits format: `<type>(<scope>): <subject>`.
- Prefer scopes such as `docs`, `code`, `phase1`, `cmake`, or the specific learning phase.
- Examples: `docs(agents): add project workflow rules`, `feat(phase2): add scatter convolution demo`, `build(cmake): add phase executable`.

## Output

- Return code first. Explanation after, only if non-obvious.
- No inline prose. Use comments sparingly - only where logic is unclear.
- No boilerplate unless explicitly requested.

## Code Rules

- Simplest working solution. No over-engineering.
- No abstractions for single-use operations.
- No speculative features or "you might also want..."
- Read the file before modifying it. Never edit blind.
- No docstrings or type annotations on code not being changed.
- No error handling for scenarios that cannot happen.
- Three similar lines is better than a premature abstraction.

## Review Rules

- State the bug. Show the fix. Stop.
- No suggestions beyond the scope of the review.
- No compliments on the code before or after the review.

## Debugging Rules

- Never speculate about a bug without reading the relevant code first.
- State what you found, where, and the fix. One pass.
- If cause is unclear: say so. Do not guess.

## Simple Formatting

- No em dashes, smart quotes, or decorative Unicode symbols.
- Plain hyphens and straight quotes only.
- Natural language characters (accented letters, CJK, etc.) are fine when the content requires them.
- Code output must be copy-paste safe.

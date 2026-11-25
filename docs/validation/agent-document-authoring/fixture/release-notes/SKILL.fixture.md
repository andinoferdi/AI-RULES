---
name: release-notes
description: Generates release notes, changelogs, release summaries, version notes and change logs by reading git history since the last tag, grouping commits by conventional-commit type, writing highlights and saving a draft file. Use for release notes, changelog, changes, what's new, version summary or release summary.
---

> This skill is run only by the release manager, who types /release-notes when a release is
> cut. No other skill calls it.

# Release notes

1. Find the last release tag with `git describe --tags --abbrev=0`.
2. List the commits since that tag with `git log <tag>..HEAD --oneline`.
3. Group the commits by conventional-commit type: feat, fix, perf, docs, chore.
4. If the repository is a monorepo that uses changesets:
   - Read every file in `.changeset/` except `config.json` and `README.md`.
   - Each file names one or more packages and a bump type (major, minor, patch).
   - Build one section per package, ordered by package name.
   - Inside each package section, order entries major, then minor, then patch.
   - Skip packages marked `"private": true` in their `package.json`.
   - If `.changeset/pre.json` exists, the repo is in pre-release mode: add the pre-release
     tag from that file to every version heading.
   - Commits that touch a package without a changeset go under "Other changes" in that
     package's section.
   - Commits that touch no package go under "Repository" at the end.
   - Use the package's `CHANGELOG.md` header style if one exists.
   - Do not delete the changeset files; the release pipeline consumes them.
   - When two changesets bump the same package, use the highest bump type.
   - Link each entry to its pull request when the changeset front matter names one.
5. Write a highlights paragraph for the three most important changes.
6. Write the notes to `RELEASE_NOTES.md`.
7. Make sure the notes look good and are complete.

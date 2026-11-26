// Adds area labels to a pull request based on the files it changes.
const repo = process.env.GITHUB_REPOSITORY;
const pr = process.env.PR_NUMBER;
const headers = {
  Authorization: `Bearer ${process.env.GITHUB_TOKEN}`,
  Accept: 'application/vnd.github+json',
};

const files = await (await fetch(`https://api.github.com/repos/${repo}/pulls/${pr}/files?per_page=100`, { headers })).json();
const labels = new Set();
for (const { filename } of files) {
  if (filename.startsWith('docs/') || filename.endsWith('.md')) labels.add('docs');
  else if (filename.startsWith('web/')) labels.add('web');
  else labels.add('api');
}

await fetch(`https://api.github.com/repos/${repo}/issues/${pr}/labels`, {
  method: 'POST',
  headers,
  body: JSON.stringify({ labels: [...labels] }),
});

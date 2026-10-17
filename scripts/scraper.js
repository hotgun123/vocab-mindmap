const fs = require('fs');
const cheerio = require('cheerio');

const content = fs.readFileSync('C:/Users/ducan/.gemini/antigravity-ide/brain/b52f2a9f-3184-414c-9142-791cca7971f6/.system_generated/steps/578/content.md', 'utf8');
const $ = cheerio.load(content);

const sentences = [];

$('p').each((i, el) => {
  const text = $(el).text().trim();
  // Example format: "Good morning! – Chào buổi sáng." or "1. Hello: Xin chào"
  // Let's use regex to match English and Vietnamese parts
  const match = text.match(/^(?:\d+\.\s*)?([A-Za-z][^:–-]+)[\s]*[:–-][\s]*(.+)$/);
  if (match) {
    const en = match[1].trim();
    const vi = match[2].trim();
    if (en.length > 3 && vi.length > 3 && en.includes(' ')) {
      sentences.push({ english: en, vietnamese: vi });
    }
  }
});

console.log('Total extracted:', sentences.length);
if (sentences.length > 0) {
  console.log(sentences.slice(0, 5));
}

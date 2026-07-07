const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

const COOKIES_FILE = path.join(__dirname, 'chatgpt_cookies.json');

async function askChatGPT(prompt) {
    const browser = await puppeteer.launch({
        headless: false,
        args: ['--no-sandbox', '--disable-setuid-sandbox'],
        defaultViewport: { width: 1280, height: 900 }
    });

    try {
        const page = await browser.newPage();

        if (fs.existsSync(COOKIES_FILE)) {
            const cookies = JSON.parse(fs.readFileSync(COOKIES_FILE, 'utf-8'));
            await page.setCookie(...cookies);
        }

        await page.goto('https://chatgpt.com', { waitUntil: 'networkidle2', timeout: 30000 });

        const loggedIn = await page.evaluate(() => !!document.querySelector('textarea'));
        if (!loggedIn) {
            console.log('Please login to ChatGPT...');
            await page.waitForSelector('textarea', { timeout: 120000 });
        }

        const cookies = await page.cookies();
        fs.writeFileSync(COOKIES_FILE, JSON.stringify(cookies, null, 2));

        await page.waitForSelector('textarea', { timeout: 10000 });
        await page.click('textarea');

        const chunks = prompt.match(/.{1,100}/g) || [prompt];
        for (const chunk of chunks) {
            await page.keyboard.type(chunk, { delay: 5 });
        }

        await page.keyboard.press('Enter');

        console.log('Waiting for ChatGPT...');
        await page.waitForFunction(() => !document.querySelector('button[aria-label="Stop generating"]'), { timeout: 180000 });
        await new Promise(r => setTimeout(r, 2000));

        const response = await page.evaluate(() => {
            const msgs = document.querySelectorAll('[data-message-author-role="assistant"]');
            return msgs[msgs.length - 1]?.innerText || '';
        });

        const newCookies = await page.cookies();
        fs.writeFileSync(COOKIES_FILE, JSON.stringify(newCookies, null, 2));

        return response;
    } catch (e) {
        console.error('ChatGPT error:', e.message);
        return null;
    } finally {
        await browser.close();
    }
}

async function findFunnyMoments(videoTitle, transcriptSegments) {
    const segmentsText = transcriptSegments.map((s, i) =>
        `[${i}] ${s.start.toFixed(1)}s - ${s.end.toFixed(1)}s: ${s.text}`
    ).join('\n');

    const prompt = `You are a comedy clip editor for YouTube Shorts. Analyze this transcript from a funny video and find the BEST moments to cut into viral shorts.

Video: ${videoTitle}

Transcript segments:
${segmentsText}

Find ${5} funniest/most engaging moments. Each clip should be 15-55 seconds long and have a complete joke or funny moment.

Return ONLY valid JSON (no markdown):
{
    "clips": [
        {
            "start": start_time_in_seconds,
            "end": end_time_in_seconds,
            "reason": "why this moment is funny/engaging",
            "title": "catchy short title for this clip",
            "hashtags": ["tag1", "tag2", "tag3"]
        }
    ]
}`;

    const response = await askChatGPT(prompt);
    if (!response) return null;

    try {
        const jsonMatch = response.match(/\{[\s\S]*\}/);
        if (jsonMatch) return JSON.parse(jsonMatch[0]);
    } catch (e) {
        console.error('JSON parse error:', e.message);
    }
    return null;
}

async function generateShortMetadata(videoTitle, clipReason, clipTitle) {
    const prompt = `Generate YouTube Shorts metadata for this clip:

Original Video: ${videoTitle}
Clip Moment: ${clipReason}
Clip Title: ${clipTitle}

Return ONLY valid JSON:
{
    "title": "catchy title max 100 chars with emoji",
    "description": "engaging description with call to follow",
    "hashtags": ["tag1", "tag2", "tag3", "tag4", "tag5", "tag6", "tag7", "tag8"]
}`;

    const response = await askChatGPT(prompt);
    if (!response) return null;

    try {
        const jsonMatch = response.match(/\{[\s\S]*\}/);
        if (jsonMatch) return JSON.parse(jsonMatch[0]);
    } catch (e) {}
    return null;
}

module.exports = { askChatGPT, findFunnyMoments, generateShortMetadata };

if (require.main === module) {
    const title = process.argv[2] || 'Funny Video';
    const segments = [{ start: 0, end: 10, text: 'test segment' }];
    findFunnyMoments(title, segments).then(r => console.log(JSON.stringify(r, null, 2)));
}

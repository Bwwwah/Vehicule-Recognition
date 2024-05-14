import crypto from 'crypto';
import fetch from 'node-fetch';
import fs from 'fs';

let previousHash = '';
let i = 1;

async function downloadImages() {
  if (!fs.existsSync('Data')) {
    fs.mkdirSync('Data');
  }

  for (let j = 0; j < 90; j++) {
    let hash;
    let buffer;

    while (true) {
      console.log("Downloading image...")
      const response = await fetch('https://download.data.grandlyon.com/files/rdata/pvo_patrimoine_voirie.pvocameracriter/CWL9018.JPG');
      buffer = await response.buffer();
      hash = crypto.createHash('sha256').update(buffer).digest('hex');

      if (hash !== previousHash) {
        break;
      }

      console.log('Hash is identical, waiting 10 seconds...');
      await new Promise(resolve => setTimeout(resolve, 10 * 1000)); // 10 * 1000 ms = 10 seconds
    }

    fs.writeFileSync(`/Data/image_${i}.jpg`, buffer);
    console.log(i + ' image downloaded');
    i++;
    previousHash = hash;

    await new Promise(resolve => setTimeout(resolve, 60 * 1000)); // 60 * 1000 ms = 1 minute
  }
}

downloadImages();
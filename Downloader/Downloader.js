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

    function getFormattedTimestamp() {
      const date = new Date();
      const year = date.getFullYear();
      const month = String(date.getMonth() + 1).padStart(2, '0');
      const day = String(date.getDate()).padStart(2, '0');
      const hours = String(date.getHours()).padStart(2, '0');
      const minutes = String(date.getMinutes()).padStart(2, '0');
      const seconds = String(date.getSeconds()).padStart(2, '0');
      return `${year}${month}${day}${hours}${minutes}${seconds}`;
    }

    fs.writeFileSync(`/Data/${getFormattedTimestamp()}.jpg`, buffer);
    console.log(i + ' image downloaded');
    i++;
    previousHash = hash;

    await new Promise(resolve => setTimeout(resolve, 60 * 1000)); // 60 * 1000 ms = 1 minute
  }
}

downloadImages();
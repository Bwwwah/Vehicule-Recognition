import fs, { existsSync } from "fs";
import fetch from "node-fetch";
import path from "path";
import { exit } from "process";

/*Token d'identification*/
const token = "16696e673bffd8a7fafe90f7a5cf1049e480b1a4";

const data = JSON.parse(fs.readFileSync("result.json", "utf8"));
const baseUrl = "https://app.heartex.com/storage-data/uploaded/?filepath=upload/67163/";

const imagesDir = "/Images";
if (!fs.existsSync(imagesDir)) {
  fs.mkdirSync(imagesDir);
}

const imagesAndAnnotations = data.images.map((dataItem) => {
  let link = dataItem.file_name;
  link = link.replace("\\", " ");
  link = link.charAt(0).toUpperCase() + link.slice(1);
  return link;
});

/*Permet de récupérer les liens des images et de les télécharger*/
async function fetchImage(link) {
  const absoluteUrl = baseUrl + link;
      const response = await fetch(absoluteUrl,  {
        headers: {
            Authorization: `Token ${token}`,
        },
      });
      if (response.ok) {
        const buffer = await response.buffer();
        const filePath = path.join(imagesDir, link.substring(link.lastIndexOf("/") + 1));
        fs.writeFileSync(filePath, buffer);
      } else {
        console.error(response.statusText);
        exit();
      }
}

async function downloadImages() {
  console.log("Downloading images... Please wait...");
  for (const link of imagesAndAnnotations) {
    await fetchImage(link);
  }
  console.log("All images downloaded");
}

downloadImages();
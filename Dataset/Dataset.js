import fs from "fs";
import fetch from "node-fetch";
import path from "path";

/*Token d'identification*/
const token = "16696e673bffd8a7fafe90f7a5cf1049e480b1a4";

const data = JSON.parse(fs.readFileSync("export.json", "utf8"));
const baseUrl = "https://app.heartex.com/storage-data/uploaded/?filepath=";

/*Permet de simplifier l'export.json*/
const imagesAndAnnotations = data.map((item) => {
  return {
    link: item.data.image,
    annotations: item.annotations.flatMap((annotation) => {
      return annotation.result.map((result) => {
        return {
          labels: result.value.rectanglelabels,
          coordinates: {
            x: result.value.x,
            y: result.value.y,
            width: result.value.width,
            height: result.value.height,
          },
        };
      });
    }),
  };
});

const imagesDir = "/Images";
if (!fs.existsSync(imagesDir)) {
  fs.mkdirSync(imagesDir);
}

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
      }
}

async function downloadImages() {
  console.log("Downloading images... Please wait...");
  let delay = 0;
  imagesAndAnnotations.forEach(async ({ link, annotations }) => {
    setTimeout(async () => {
      fetchImage(link);
    }, delay);
    delay += 200;
  });
  console.log("All images downloaded");
}

downloadImages();

const dataset = imagesAndAnnotations.map(({ link, annotations }, index) => ({
  link: `Images/${link.substring(link.lastIndexOf("/") + 1)}`,
  annotations,
}));

const json = JSON.stringify(dataset, null, 2);
fs.writeFileSync('dataset.json', json);
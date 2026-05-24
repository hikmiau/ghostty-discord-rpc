require("dotenv").config();

const client = require("discord-rich-presence")(process.env.CLIENT_ID);
const path = require("path");
const fs = require("fs");
const { execSync } = require("child_process");

const startTimestamp = Date.now();
const pwdFile = `${process.env.HOME}/.cache/kitty-rpc-pwd`;

const config = {
  details: "Using Kitty",
  fallbackProject: "Terminal",

  largeImageKey: "your_large_image_asset_key",
  largeImageText: "Your large image hover text",

  smallImageKey: "your_small_image_asset_key",
  smallImageText: "Your small image hover text",
};

function isNvimRunning() {
  try {
    execSync("pgrep -x nvim", { stdio: "ignore" });
    return true;
  } catch {
    return false;
  }
}

function getCurrentProject() {
  try {
    const currentDir = fs.readFileSync(pwdFile, "utf8").trim();
    return path.basename(currentDir) || "Home";
  } catch {
    return config.fallbackProject;
  }
}

function updatePresence() {
  if (isNvimRunning()) {
    client.disconnect?.();
    return;
  }

  client.updatePresence({
    details: config.details,
    state: `Project: ${getCurrentProject()}`,
    startTimestamp,

    largeImageKey: config.largeImageKey,
    largeImageText: config.largeImageText,

    smallImageKey: config.smallImageKey,
    smallImageText: config.smallImageText,
  });
}

updatePresence();
setInterval(updatePresence, 5000);

console.log("Kitty Discord RPC running.");

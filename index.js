const client = require("discord-rich-presence")("1507869608709722142");
const path = require("path");
const fs = require("fs");
const { execSync } = require("child_process");

const startTimestamp = Date.now();
const pwdFile = `${process.env.HOME}/.cache/ghostty-rpc-pwd`;

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
    return "Kitty";
  }
}

function updatePresence() {
  if (isNvimRunning()) {
    client.disconnect?.();
    return;
  }

  client.updatePresence({
    details: "Using Kitty",
    state: `Project: ${getCurrentProject()}`,
    startTimestamp,
    largeImageKey: "kitty",
    largeImageText: "Kitty Terminal",
    smallImageKey: "arch",
    smallImageText: "Arch Linux",
  });
}

updatePresence();
setInterval(updatePresence, 5000);

console.log("Kitty Discord RPC running.");

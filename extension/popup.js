document.getElementById("trigger").addEventListener("click", () => {
  chrome.runtime.sendMessage("trigger_native");
});

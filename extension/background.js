// listen to visited url
chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  // on visit url: https://www.linkedin.com/
  if (
    changeInfo.status === "complete" &&
    /^https:\/\/www\.linkedin\.com\/*/.test(tab.url)
  ) {
    chrome.scripting
      .insertCSS({ target: { tabId: tabId }, files: ["./styles/linkedin.css"] })
      .then(() =>
        chrome.scripting.executeScript({
          target: { tabId: tabId },
          files: ["./scripts/linkedin.js"],
        })
      )
      .catch((err) => console.log(err));
  }
});

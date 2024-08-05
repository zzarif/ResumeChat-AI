// focus on contenteditable div and render resumechat buttons
document.addEventListener("focusin", (e) => {
  const viewOnFocus = e.target;
  // if the focused node is div and has attribute contenteditable
  if (
    viewOnFocus.nodeName === "DIV" &&
    viewOnFocus.hasAttribute("contenteditable")
  ) {
    const form_comments = viewOnFocus.closest(
      "form.comments-comment-box__form"
    );
    // if the buttons already don't exist
    if (
      form_comments &&
      form_comments.querySelector("div.resumechat-linkedin-container") === null
    ) {
      const btnLike = getResumeChatButton(0, " 👍 "); // like
      const btnDislike = getResumeChatButton(1, " 👎 "); // dislike
      const btnSupport = getResumeChatButton(2, "❤️ Support"); // support
      const btnJoke = getResumeChatButton(3, "😂 Funny"); //joke
      const btnQuestion = getResumeChatButton(4, "❓ Question"); // question

      // button parent conatiner
      const container = document.createElement("div");
      container.className = "resumechat-linkedin-container";

      // insert buttons inside the parent container
      container.appendChild(btnLike);
      container.appendChild(btnDislike);
      container.appendChild(btnSupport);
      container.appendChild(btnJoke);
      container.appendChild(btnQuestion);

      form_comments.appendChild(container);
    }
  }
});

var commenter = "";
var comment = "";
document.addEventListener("click", (e) => {
  const viewClicked = e.target;
  if (viewClicked.nodeName === "SPAN" && viewClicked.textContent === "Reply") {
    // name of the commenter
    commenter = viewClicked
      .closest("article.comments-comment-item")
      .querySelector("span.comments-post-meta__name-text")
      .textContent.trim();
    // content of the comment
    comment = viewClicked
      .closest("article.comments-comment-item")
      .querySelector("span.comments-comment-item__main-content")
      .textContent.trim();
  }
});

/**
 * function to generate RESUME_CHAT button
 * @param "which" : which button (like/support/...)
 * @param "text" : text of the button
 * @returns generated button
 */
function getResumeChatButton(which, text) {
  const rmButton = document.createElement("button");
  rmButton.className = "resumechat-linkedin-btn";
  const txtNode = document.createTextNode(text);
  rmButton.appendChild(txtNode);
  rmButton.addEventListener("click", (e) => {
    e.preventDefault();
    generateComment(e.target, which);
  });
  return rmButton;
}

/**
 * function to get poster, caption
 * send them to the server and
 * fetch ChatGPT response
 * @param "viewClicked" : clicked button
 * @param "type" : type of reaction
 */
async function generateComment(viewClicked, type) {
  flipButtonState(viewClicked, true);
  const lnkdnAPIBaseURL =
    "https://api.server.com/linkedin/";
  try {
    const view_feed_update = viewClicked.closest("div.feed-shared-update-v2");
    const view_reusable_search = viewClicked.closest(
      "li.reusable-search__result-container"
    );

    var poster, caption;
    if (view_feed_update) {
      // name of the poster
      poster = view_feed_update
        .querySelector("span.update-components-actor__name")
        .querySelector("span")
        .textContent.trim();
      // caption of the post
      caption = view_feed_update
        .querySelector("div.update-components-text")
        .textContent.trim();
    } else {
      // name of the poster
      poster = view_reusable_search
        .querySelector("span.entity-result__title-text")
        .querySelector("span")
        .firstChild.textContent.trim();
      // caption of the post
      caption = view_reusable_search
        .querySelector("div.entity-result__content-inner-container")
        .textContent.trim();
    }

    // contentEditable comment box to put response
    const contentEditableDiv = viewClicked
      .closest("form.comments-comment-box__form")
      .querySelector("div.ql-editor");

    showLoadingAnimation(contentEditableDiv);

    // COMMENTING to the post
    if (viewClicked.closest("article.comments-comment-item") === null) {
      // default comment (type 0 to 4)
      await fetch(lnkdnAPIBaseURL + "default", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          poster: poster,
          caption: caption,
          type: type,
        }),
      })
        .then((res) => res.json())
        .then((data) => {
          // https://stackoverflow.com/a/72935050
          contentEditableDiv.focus();
          document.execCommand("selectAll", false);
          document.execCommand("delete", false);
          document.execCommand("insertText", false, data.comment);
        })
        .finally(() => removeAnimation(contentEditableDiv));
    }

    // REPLYING to a comment
    else {
      // default reply (type 0 to 4)
      await fetch(lnkdnAPIBaseURL + "default-reply", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          poster: poster,
          caption: caption,
          commenter: commenter,
          comment: comment,
          type: type,
        }),
      })
        .then((res) => res.json())
        .then((data) => {
          // https://stackoverflow.com/a/72935050
          contentEditableDiv.focus();
          document.execCommand("selectAll", false);
          document.execCommand("delete", false);
          document.execCommand("insertText", false, data.comment);
        })
        .finally(() => removeAnimation(contentEditableDiv));
    }
  } catch (err) {
    alert("RESUME_CHAT: Please try again after a minute!");
  } finally {
    flipButtonState(viewClicked, false);
  }
}

function showLoadingAnimation(onView) {
  const dotStage = document.createElement("div");
  dotStage.className = "resumechat-dot-stage";
  const dotFlashing = document.createElement("div");
  dotFlashing.className = "resumechat-dot-flashing";
  dotStage.appendChild(dotFlashing);
  onView.parentNode.parentNode.appendChild(dotStage);
}

function removeAnimation(fromView) {
  const lastChild = fromView.parentNode.parentNode.lastChild;
  if (lastChild.className === "resumechat-dot-stage")
    fromView.parentNode.parentNode.removeChild(lastChild);
}

function flipButtonState(viewClicked, active) {
  const pDiv = viewClicked.parentNode;
  for (i = 0; i < pDiv.childElementCount; i++)
    pDiv.children[i].disabled = active;
}

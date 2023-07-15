const dropdownMenu = document.querySelector(".dropdown-menu");
const dropdownButton = document.querySelector(".dropdown-button");

if (dropdownButton) {
  dropdownButton.addEventListener("click", () => {
    dropdownMenu.classList.toggle("show");
  });
}

// Scroll to Bottom
const conversationThread = document.querySelector(".feed__box");
if (conversationThread) conversationThread.scrollTop = conversationThread.scrollHeight;


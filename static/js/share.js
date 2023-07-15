// copy
const shareBtn = document.querySelector("#share");

shareBtn.addEventListener("click",(e)=>{
  const url = e.target.dataset.url;
navigator.clipboard.writeText(url);
toast('Copied to Clipboard', 'success', 1000)
})
window.toast = function(str, extraClass = '', timeout = 3000) {
  const div = document.createElement('div')
  div.className = 'toast ' + extraClass
  div.innerHTML = str
  setTimeout(function(){
    div.remove()
  }, timeout);
  document.body.appendChild(div);
}
//텍스트 입력없으면 버튼못누름 
const inputBox = document.querySelector('#title');
function activateBtn() { 
  const btn = document.querySelector('#btn_create'),
  title = document.querySelector('#title').value,
  checktext = /^[ㄱ-ㅎ|가-힣|a-z|A-Z|0-9|\s]*$/; // 한글숫자영어만(공백포함) 입력가능
  btn.disabled = !(checktext.test(title) && (title.length>2));
}
inputBox.addEventListener('keyup', activateBtn);

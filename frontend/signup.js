const form = document.querySelector("#signup-from");

const checkPassword = () => {
  const formData = new FormData(form);
  const password1 = formData.get("password");
  const password2 = formData.get("password2");
  if (password1 == password2) {
    return true;
  } else return false;
};
const handleSubmit = async (event) => {
  event.preventDefault();
  //폼 데이터를 가져옴
  const formData = new FormData(form);
  //sha256으로 보안을 하고
  const sha256Pw = sha256(formData.get("password"));
  //패스워드 안에 넣어줌
  formData.set("password", sha256Pw);

  const div = document.querySelector("#info");

  if (checkPassword()) {
    const res = await fetch("/signup", {
      method: "post",
      body: formData,
    });
    //서버에서 응답을 줬을 때만
    const data = await res.json();
    if (data === "200") {
      div.innerText = "회원가입에 성공";
      div.style.color = "blue";
      window.location.pathname = "/login.html";
    }
  } else {
    div.innerText = "비밀번호가 같지 않습니다";
    div.stye.color = "red";
  }
};

form.addEventListener("submit", handleSubmit);

const form = document.querySelector("#signup-form");
//비밀번호가 같은지 판단하는 로직
const checkPassword = () => {
  const formData = new FormData(form);
  const password1 = formData.get("password");
  const password2 = formData.get("password2");
  if (password1 === password2) {
    return true;
  } else return false;
};

const handleSubmit = async (event) => {
  event.preventDefault();
  //폼 데이터를 가져옴
  const formData = new FormData(form);
  // 보안을 하고(해시)
  const sha256Password = sha256(formData.get("password"));
  //패스워드 안에 넣어줌
  formData.set("password", sha256Password);

  const div = document.querySelector("#info");
  if (checkPassword()) {
    const res = await fetch("/signup", {
      method: "POST",
      body: formData,
    });
    //서버에서 응답이 온 후에 200이라는 값이면 성공했으므로 멘트는 보내줌
    const data = await res.json();
    if (data === "200") {
      alert("성공");
      window.location.pathname = "/login.html";
    }
  } else {
    div.innerText = "비밀번호가 다릅니다";
    div.style.color = "red";
  }
};
form.addEventListener("submit", handleSubmit);

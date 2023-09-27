const form = document.querySelector("#login-form");

const handleSubmit = async (event) => {
  event.preventDefault();
  //폼 데이터를 가져옴
  const formData = new FormData(form);
  // 보안을 하고(해시)
  const sha256Password = sha256(formData.get("password"));
  //패스워드 안에 넣어줌
  formData.set("password", sha256Password);

  const res = await fetch("/login", {
    method: "POST",
    body: formData,
  });
  //서버에서 응답이 온 후에 200이라는 값이면 성공했으므로 멘트는 보내줌
  //서버에서 보내 주는 값이 아님 data값은 문자열
  const data = await res.json();
  const accessTocken = data.access_token;
  //토큰 값을 로컬 스토리지에 넣어주는 것
  window.localStorage.setItem("token", accessTocken);
  alert("로그인완료");

  window.location.pathname = "/";
  /* const btn = document.createElement("button");
  btn.innerText = "상품 가져오기";
  btn.addEventListener("click", async () => {
    const res = await fetch("/items", {
      //401에러가 발생하기 때문에 Authorization을 넣어줌
      headers: {
        Authorization: `Bearer ${accessTocken}`, //authorization이라는 헤더를 넣을 건데 prefix인 bearer을 써서 보냄
      },
    });
    const data = await res.json();
    console.log(data);
  });
  infoDiv.appendChild(btn);*/
};
form.addEventListener("submit", handleSubmit);

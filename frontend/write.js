const form = document.getElementById("write-form");

const handleSubmitForm = async (event) => {
  event.preventDefault();
  const body = new FormData(form);
  //세계시간기준으로 보냄
  body.append("insertAt", new Date().getTime());
  //try안에서 로직을 실행하다가 에러가 발생하면 catch를 실행
  try {
    const res = await fetch("/items", {
      method: "POST",
      //폼데이터형식으로 보냄
      body,
    });
    const data = await res.json();
    if (data == "200") window.location.pathname = "/"; //윈도우의 경로값을 변경
  } catch (e) {
    console.error();
  }
};

form.addEventListener("submit", handleSubmitForm);

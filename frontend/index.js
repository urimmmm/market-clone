const calcuTime = (timestamp) => {
  //한국시간 기준으로 받아옴
  const curTime = new Date().getTime() - 9 * 60 * 60 * 1000;
  const time = new Date(curTime - timestamp);
  const hour = time.getHours();
  const min = time.getMinutes();
  const sec = time.getSeconds();

  if (hour > 0) return `${hour} 시간 전`;
  else if (min > 0) return `${min} 분 전`;
  else if (sec > 0) return `${sec}초 전`;
  else "방금 전";
};
const renderData = (data) => {
  const main = document.querySelector("main");
  //배열에만 쓸 수 있는 구문으로 각각의 배열 내부에 있는 항목을 돌면서 그거에 대한 값을 넣어줌
  data.reverse().forEach(async (obj) => {
    const div = document.createElement("div");
    div.className = "item-list";

    const imageDiv = document.createElement("div");
    imageDiv.className = "item-list__img";

    const img = document.createElement("img");
    //파이썬에서 image에 대한 blob을 받아와서 src에 넣어줌
    const res = await fetch(`/images/${obj.id}`);
    const blob = await res.blob();
    const url = URL.createObjectURL(blob);
    img.src = url;

    const InfoDiv = document.createElement("div");
    InfoDiv.className = "item-list__info";

    const InfoTitleDiv = document.createElement("div");
    InfoTitleDiv.className = " item-list__info-title";
    InfoTitleDiv.innerText = obj.title;

    const InfoMetaDiv = document.createElement("div");
    InfoMetaDiv.className = "item-list__info-meta";
    InfoMetaDiv.innerText = obj.place + " " + calcuTime(obj.insertAt);

    const InfoPriceDiv = document.createElement("div");
    InfoPriceDiv.className = "item-list__info-price";
    InfoPriceDiv.innerText = obj.price;

    imageDiv.appendChild(img);
    InfoDiv.appendChild(InfoTitleDiv);
    InfoDiv.appendChild(InfoMetaDiv);
    InfoDiv.appendChild(InfoPriceDiv);
    div.appendChild(imageDiv);
    div.appendChild(InfoDiv);

    main.appendChild(div);
  });
};

//서버에서 데이터를 받아와서 리스트 형식으로 보내주는 내용
const fetchList = async () => {
  //파이썬에 있는 /items와 다름 (파이썬은 POST메소드이기 때문)
  const res = await fetch("/items");
  const data = await res.json();
  renderData(data);
};

fetchList();

<script>
  import { getDatabase, ref, push } from "firebase/database";
  import {
    getStorage,
    ref as refImage,
    uploadBytes,
    getDownloadURL,
  } from "firebase/storage";
  import Nav from "../components/Nav.svelte";

  let title;
  let price;
  let description;
  let place;
  let files;

  const storage = getStorage();
  const db = getDatabase();

  function writeUserData(imgUrl) {
    push(ref(db, "items/"), {
      title,
      price,
      description,
      place,
      insertAt: new Date().getTime(),
      imgUrl,
    });
    alert("글쓰기 완료");
    window.location.hash = "/";
  }

  const uploadFile = async () => {
    const file = files[0];
    const name = file.name;
    const imgRef = refImage(storage, name);
    //이미지 업로드
    await uploadBytes(imgRef, file);
    const url = await getDownloadURL(imgRef);
    return url;
  };
  const handleSubmit = async () => {
    const url = await uploadFile();
    writeUserData(url);
  };
</script>

<!--데이터가 전송이 되었을 때 데이터를 서버쪽으로 보냄-->
<form id="write-form" on:submit|preventDefault={handleSubmit}>
  <div>
    <label for="image">이미지</label>
    <input type="file" bind:files id="image" name="image" />
  </div>
  <div>
    <label for="title">제목</label>
    <!--bind를 이용해 값을 연동시킴-->
    <input type="text" id="title" name="title" bind:value={title} />
  </div>
  <div>
    <label for="price">가격</label>
    <input type="number" id="price" name="price" bind:value={price} />
  </div>
  <div>
    <label for="description">설명</label>
    <input
      type="text"
      id="description"
      name="description"
      bind:value={description}
    />
  </div>
  <div>
    <label for="place">장소</label>
    <input type="text" id="place" name="place" bind:value={place} />
  </div>
  <div>
    <button class="write-button" type="submit">완료</button>
  </div>
</form>
<Nav location="write" />

<!--파일 내에서만 스타일이 적용되기 때문에 다른 곳에 writebutton을 사용해도 상관없다-->
<style>
  .write-button {
    background-color: yellow;
  }
</style>

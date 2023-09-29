<script>
  //각각 svelte파일로 나눠서 합치는 모듈방식
  import Login from "./pages/Login.svelte";
  import Main from "./pages/Main.svelte";
  import Notfound from "./pages/Notfound.svelte";
  import Signup from "./pages/Signup.svelte";
  import Write from "./pages/Write.svelte";
  import Router from "svelte-spa-router";
  import "./css/style.css";
  import { user$ } from "./store";
  import {
    GoogleAuthProvider,
    getAuth,
    signInWithCredential,
  } from "firebase/auth";
  import { onMount } from "svelte";
  import Loading from "./pages/Loading.svelte";

  const auth = getAuth();

  const checkLogin = async () => {
    const token = localStorage.getItem("token");
    if (!token) return (isLoading = false);

    const credential = GoogleAuthProvider.credential(null, token);
    const result = await signInWithCredential(auth, credential);
    const user = result.user;
    user$.set(user);
    isLoading = false;
  };

  const provider = new GoogleAuthProvider();
  provider.addScope("http://www.googleapis.com/auth/contacts.readonly");

  let isLoading = true;
  let login = false;

  const routes = {
    "/": Main,
    "/signup": Signup,
    "/write": Write,
    "*": Notfound,
  };

  onMount(() => checkLogin());
</script>

{#if !login}
  <Login />
{:else}
  <Router {routes} />
{/if}

import { initializeApp } from "firebase/app";
import { getDatabase } from "firebase/database";
import { getStorage } from "firebase/storage";
import { getAuth } from "firebase/auth";

const firebaseConfig = {
  apiKey: "AIzaSyCfBz1RZ8_E6V1_zFPoQ0ckqrz0pOoDrE0",
  authDomain: "corrot-clone.firebaseapp.com",
  databaseURL:
    "https://corrot-clone-default-rtdb.asia-southeast1.firebasedatabase.app",
  projectId: "corrot-clone",
  storageBucket: "buckets/corrot-clone.appspot.com",
  messagingSenderId: "229097102070",
  appId: "1:229097102070:web:e563796f20ac35242b6ad7",
};

const app = initializeApp(firebaseConfig);

// Initialize Realtime Database and get a reference to the service
const database = getDatabase(app);
const storage = getStorage(app);
const auth = getAuth(app);

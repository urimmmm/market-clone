from fastapi import FastAPI,UploadFile,Form,Response
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.staticfiles import StaticFiles
from fastapi_login import LoginManager
from typing import Annotated
import sqlite3


con = sqlite3.connect('db.db', check_same_thread=False)
cur = con.cursor() # 특정 인서트하거나 셀렉트할 때 사용


app = FastAPI()

cur.execute(f"""
            CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            image BLOB,
            price INTEGER NOT NULL,
            description TEXT,
            place TEXT NOT NULL,
            insertAt INTEGER NOT NULL
            );
            """)



@app.post("/signup")
def signup(id:Annotated[str, Form()], 
           password:Annotated[str, Form()],
           name: Annotated[str, Form()],
           email:Annotated[str, Form()]):
    #기존에 회원가입이 되어있는 사람도 또 가입이 되기때문에 안되도록 해보기!!!!
    # DB에 저장시킴
    cur.execute(f"""
                INSERT INTO users(id, name, email, password)
                Values('{id}', '{name}', '{email}', '{password}')
                """)
    # DB에 들어갔는지 확인하기 위해서 커밋해줌
    con.commit()
    return "200"




@app.post('/items')
async def create_item(image:UploadFile,
                title:Annotated[str,Form()], #폼데이터 형식으로 문자열로 옴
                price:Annotated[int,Form()],
                description:Annotated[str,Form()],
                place:Annotated[str,Form()],
                insertAt:Annotated[str,Form()]):
    
    image_bytes = await image.read() #이미지데이터가 크기 때문에 읽을 시간이 필요함
    cur.execute(f"""
                INSERT INTO items (title, image, price, description, place, insertAt)
                VALUES ('{title}', '{image_bytes.hex()}', '{price}', '{description}', '{place}', '{insertAt}')
                """)
    con.commit()
    return '200'
    
@app.get("/items")
async def get_items():
    con.row_factory = sqlite3.Row #데이터값 외에 컬럼명도 가져옴
    cur = con.cursor()
    rows = cur.execute(f""" 
                       SELECT * FROM items
                       """).fetchall()
    #rows들 중에 각 배열을 돌면서 배열을 객체(dictionary) 형태로 만들어줌
    return JSONResponse(jsonable_encoder(dict(row) for row in rows))
#이미지 응답받는
@app.get("/images/{item_id}")
async def get_image(item_id):
    cur=con.cursor()
    #특정아이디에 맞는 이미지 컬럼만 가져오기
    #image_byte는 16진법으로 표시되고 있음 
    image_byte = cur.execute(f"""
                             SELECT image FROM items WHERE id={item_id}
                             """).fetchone()[0]
    #16진법으로 된거를 바꿔서 보내겠다
    return Response(content=bytes.fromhex(image_byte), media_type="image/*")


app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")

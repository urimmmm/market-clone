from fastapi import FastAPI,UploadFile,Form,Response,Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.staticfiles import StaticFiles
from fastapi_login import LoginManager
# 유효하지 않는 계정을 에러처리할 수 있는 문법 
from fastapi_login.exceptions import InvalidCredentialsException
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


#sercret - 엑세스 토큰을 어떻게 인코딩하는지를 정함
#반대로 디코딩도 가능하기 때문에 시크릿키 노출시키면 언제든지 jwt를 해석할 수 있다
SERCRET = "super-coding"
# sercret과 로그인 경로에서 적당한 엑세스 토큰을 만드는 라이브러리
manager = LoginManager(SERCRET, "/login")

#로그인 매니저가 query_user를 사용할 때 키를 같이 조회함
@manager.user_loader()
def query_user(data):
    WHERE_STATEMENTS = f'id="{data}"'
    if type(data) == dict:
        WHERE_STATEMENTS = f'''id="{data['id']}"'''
    con.row_factory = sqlite3.Row #데이터 컬럼명을 가져옴
    cur = con.cursor()
    user = cur.execute(f"""
                       SELECT * from users WHERE {WHERE_STATEMENTS}
                       """).fetchone()
    return user

@app.post("/login")
def login(id:Annotated[str, Form()], 
           password:Annotated[str, Form()]):
    # 쿼리유저를 이용해서 users를 받아옴
    user = query_user(id)
    print(user['password'])
    # 해당 유저가 존재하는지 아닌지 판단하는 로직
    if not user: 
        # 에러메세지 raise 401
        raise InvalidCredentialsException
    elif password != user['password']:
        raise InvalidCredentialsException
    
    access_token = manager.create_access_token(data={
        'sub' : {
        'id':user['id'],
        'name':user['name'],
        'email':user['email']
        }
    })
    # 값을 200을 주지 않아도 서버내에서 200값을 리턴해줌
    return {'access_token':access_token}


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
async def get_items(user=Depends(manager)): # 유저가 인증된 상태에서만 아이템을 가져온다
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

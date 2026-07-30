from fastapi import APIRouter,Query,Body

router  = APIRouter(prefix='/user')

@router.get('/')
def get_user(size:int = Query(default=10),page:int=Query(default=1)):
    print(size,page)
    return {
        'code':200
    }

@router.post('/add')
def add_user(
    email:str = Body(...,min_length=1,max_length=10,description="邮箱不能为空!"),
    name:str=Body(...,min_length=1,max_length=10,description="姓名不能为空!")):
    return {
        'code':200,
        'data':{
            "email":email,
            "name":name
        }
    }
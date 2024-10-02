from fastapi import FastAPI
import uvicorn

from app.database.orm import create_tables, check_exist_db
from app.api.endpoints import router as admin_router, colors_and_breeds_router

app = FastAPI(title='API для администратора онлайн выставки котят')
app.include_router(admin_router)
app.include_router(colors_and_breeds_router)

if __name__ == '__main__':
    
    try:
        check_exist_db()
    except Exception:
        create_tables()
    
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)
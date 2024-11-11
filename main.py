from fastapi import FastAPI, File, UploadFile, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uuid
import shutil
import os
import subprocess
from pathlib import Path

app = FastAPI()

# 允许的源
origins = [
    "http://localhost:8000",  # 前端Vue应用的URL
    "http://localhost:8080",  # 前端Vue应用的URL
    "http://127.0.0.1:8000",
    "http://0.0.0.0:8000",
    "http://0.0.0.0:5173",
    "http://127.0.0.1:5173",
]

# 添加 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            # 允许访问的源
    allow_credentials=True,            # 允许传递身份验证信息，如 Cookies
    allow_methods=["*"],               # 允许所有HTTP方法
    allow_headers=["*"],               # 允许所有HTTP头部
)

UPLOAD_DIR = Path("backend/uploads")
RESULTS_DIR = Path("backend/results")

# 确保目录存在
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

# 文件上传和处理接口
@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    # 为每次请求生成唯一ID
    file_id = str(uuid.uuid4())
    upload_path = UPLOAD_DIR / f"{file_id}.zip"
    result_path = RESULTS_DIR / file_id

    # 保存上传文件
    with open(upload_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # 调用 C++ 程序处理文件
    result_path.mkdir(exist_ok=True)
    try:
#        subprocess.run(["./process_data", str(upload_path), str(result_path)], check=True)
        subprocess.run(["./process_data", str(result_path)], check=True)
    except subprocess.CalledProcessError:
        raise HTTPException(status_code=500, detail="数据处理失败")

    # 返回预览和下载链接
    view_path = f"/view/{file_id}/index.html"
    #view_path = f"/view/index.html"
    download_path = f"/download/{file_id}.zip"
    return JSONResponse(content={"view_path": view_path, "download_path": download_path})

# 提供下载接口
@app.get("/download/{file_id}.zip", response_class=FileResponse)
async def download_result(file_id: str):
    result_dir = RESULTS_DIR / file_id
    zip_path = result_dir.with_suffix('.zip')

    if not result_dir.exists():
        raise HTTPException(status_code=404, detail="结果未找到")

    # 压缩文件夹以供下载
    if not zip_path.exists():
        shutil.make_archive(str(result_dir), 'zip', result_dir)

    return FileResponse(zip_path, filename=f"{file_id}.zip", media_type="application/zip")

# 提供预览接口（静态文件服务）
@app.get("/view/{file_id}/{filename:path}")
async def view_file(file_id: str, filename: str):
    file_path = RESULTS_DIR / file_id / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="文件未找到")
    return FileResponse(file_path)
# 上传文件并调用C++程序处理
#@# 文件上传和处理接口
#@app.post("/upload/")
#async def upload_file(file: UploadFile = File(...)):
#    # 为每次请求生成唯一ID
#    file_id = str(uuid.uuid4())
#    upload_path = UPLOAD_DIR / f"{file_id}.zip"
#    result_path = RESULTS_DIR / file_id
#
#    # 保存上传文件
#    with open(upload_path, "wb") as buffer:
#        shutil.copyfileobj(file.file, buffer)
#
#    # 调用 C++ 程序处理文件
#    result_path.mkdir(exist_ok=True)
#    try:
#        subprocess.run(["./process_data", str(upload_path), str(result_path)], check=True)
#    except subprocess.CalledProcessError:
#        raise HTTPException(status_code=500, detail="数据处理失败")
#
#    # 返回预览和下载链接
#    view_path = f"/view/{file_id}/index.html"
#    download_path = f"/download/{file_id}.zip"
#    return JSONResponse(content={"view_path": view_path, "download_path": download_path})
#
## 提供下载接口
#@app.get("/download/{file_id}.zip", response_class=FileResponse)
#async def download_result(file_id: str):
#    result_dir = RESULTS_DIR / file_id
#    zip_path = result_dir.with_suffix('.zip')
#
#    if not result_dir.exists():
#        raise HTTPException(status_code=404, detail="结果未找到")
#
#    # 压缩文件夹以供下载
#    if not zip_path.exists():
#        shutil.make_archive(str(result_dir), 'zip', result_dir)
#
#    return FileResponse(zip_path, filename=f"{file_id}.zip", media_type="application/zip")
#
## 提供预览接口（静态文件服务）
#@app.get("/view/{file_id}/{filename:path}")
#async def view_file(file_id: str, filename: str):
#    file_path = RESULTS_DIR / file_id / filename
#    if not file_path.exists():
#        raise HTTPException(status_code=404, detail="文件未找到")
#    return FileResponse(file_path)app.post("/upload/")
#async def upload_file(file: UploadFile = File(...)):
#    file_id = str(uuid.uuid4())
#    upload_path = UPLOAD_DIR / f"{file_id}.zip"
#    
#    # 保存上传的文件
#    with open(upload_path, "wb") as buffer:
#        shutil.copyfileobj(file.file, buffer)
#    
#    # 调用C++程序处理数据
#    result_path = RESULTS_DIR / file_id
#    result_path.mkdir(parents=True, exist_ok=True)
#    subprocess.run(["./process_data", str(upload_path), str(result_path)], check=True)
#    
#    return {"file_id": file_id, "result_path": f"/view/{file_id}/index.html"}
#
## 生成的index.html页面展示
#@app.get("/view/{file_id}/index.html", response_class=HTMLResponse)
#async def view_result(file_id: str):
#    index_path = RESULTS_DIR / file_id / "index.html"
#    if index_path.exists():
#        return index_path.read_text()
#    return HTMLResponse(content="Result not found", status_code=404)
#
## 下载生成文件
#@app.get("/download/{file_id}/")
#async def download_result(file_id: str):
#    result_zip = RESULTS_DIR / f"{file_id}.zip"
#    shutil.make_archive(result_zip.with_suffix(''), 'zip', RESULTS_DIR / file_id)
#    return FileResponse(result_zip, filename=f"{file_id}.zip", media_type="application/zip")
#
#app.mount("/results", StaticFiles(directory="backend/results"), name="results")

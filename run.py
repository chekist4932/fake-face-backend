import uvicorn

if __name__ == "__main__":
    uvicorn.run("main:app", port=56000, host='0.0.0.0', reload=True)
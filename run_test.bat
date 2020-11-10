REM kill all docker process
@ECHO OFF
FOR /f "tokens=*" %%i IN ('docker ps -q') DO docker kill %%i

REM build docker image
docker build -t myimage .


REM run docker image
docker run -d -p 5000:5000 myimage

REM Wait for server to be ready
PING localhost -n 10 >NUL

REM perfrom MLInference test
curl -X POST -F file=@dog1.jpg -F file=@dog2.jpg -F file=@cat1.jpg -F file=@cat2.jpg -F file=@squirrel1.jpg http://localhost:5000/predict

pause
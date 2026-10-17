@echo off
chcp 65001 >nul
echo ===================================================
echo   VOCABULARY MASTER - 3000 TU VUNG THEO CHU DE
echo ===================================================
echo.
echo Dang khoi dong web server local tai http://localhost:8080...
echo Ban co the mo truc tiep file index.html hoac truy cap dia chi web ben duoi.
echo.

start "" "http://localhost:8080/index.html"
python -m http.server 8080
if %errorlevel% neq 0 (
    echo Khong tim thay Python de mo server, he thong se mo truc tiep index.html trong trinh duyet...
    start "" "index.html"
)
pause

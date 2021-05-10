### 编译

```bash
# 国内源
GOPROXY=https://goproxy.cn

# 交叉编译
# CGO_ENABLED=0
CGO_ENABLED=0 GOOS=windows GOARCH=amd64 go build main.go

# CGO_ENABLED=1 需要下载mingw
brew install mingw-w64
CGO_ENABLED=1 CC=x86_64-w64-mingw32-gcc CXX=x86_64-w64-mingw32-g++ GOOS=windows GOARCH=amd64 go build
CGO_ENABLED=1 CC=i686-w64-mingw32-gcc CXX=i686-w64-mingw32-g++ GOOS=windows GOARCH=386 go build 
```


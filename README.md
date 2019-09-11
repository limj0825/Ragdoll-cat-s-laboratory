# Welcome To Ragdoll Cat's Laboratory
# 安装
1、安装mongodb
* 通过系统包管理器安装

    如 brew (mac), apt-get (ubuntu)
* 手动安装
    
    curl -O https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-4.0.3.tgz
    
    tar -zxvf mongodb-linux-x86_64-4.0.3.tgz
    
    mv mongodb-linux-x86_64-4.0.3/ /usr/local/mongodb
    
    export PATH=\<mongodb-install-directory>/bin:$PATH
    
    \<mongodb-install-directory> 为你 MongoDB 的安装路径。如本文的 /usr/local/mongodb 。
    
    mkdir -p /data/db
    
    启动服务 mongod
    
    ***
    
    mongodb服务一直挂着
    
    vim ~/.bashrc
    
    加入 export PATH=/usr/local/mongodb/bin:$PATH
    
    source ~/.bashrc
    
    mongod --fork --logpath=/data/logs
    
2、安装python的依赖

```shell script
pip install -r requirements.txt
```

3、启动
```shell script
python3 app/run.py
```
4、启动挂在后台
```shell script
nohup python3 run.py > out.txt &
```




# 继续开发代码

## 安装node.js

```shell script
cd /usr/local/src
wget https://nodejs.org/dist/v10.16.3/node-v10.16.3-linux-x64.tar.xz
xz -d node-v10.16.3-linux-x64.tar.xz
tar -xf node-v10.16.3-linux-x64.tar
```
* 确认nodejs的路径  我这里部署到了  ~/node-v10.16.3-linux-x64
```shell script
ln -s ~/node-v10.16.3-linux-x64/bin/node /usr/bin/node
ln -s ~/node-v10.16.3-linux-x64/bin/npm /usr/bin/npm
ln -s ~/node-v10.16.3-linux-x64/bin/npx /usr/bin/npx
```
## 压缩react代码
```shell script
npm init -y
npm install terser
npx terser -c -m -o like_button.min.js -- like_button.js
```
上述命令会用like_button.js生成一个新的压缩后的文件like_button.min.js

## 自动压缩JSX
进入你的项目文件夹下
```shell script
npm init -y
npm install babel-cli@6 babel-preset-react-app@3
```
在static/javascript目录下运行
```shell script
mkdir src
npx babel --watch src --out-dir . --presets react-app/prod
```
创建一个src的目录
里面是JSX的源码  这个服务会自动把里面的代码转化为适用于普通浏览器的代码
编辑里面的代码  转换过程将自动执行

源文件 => 新文件

src/test.js => test.js

可以用以下语句使服务在后台运行
```shell script
nohup npx babel --watch src --out-dir . --presets react-app/prod > /dev/null &
```

FROM nginx:alpine

# 复制静态文件
COPY . /usr/share/nginx/html

# 复制自定义nginx配置
COPY nginx.conf /etc/nginx/nginx.conf

# 暴露端口
EXPOSE 80

# 启动nginx
CMD ["nginx", "-g", "daemon off;"]

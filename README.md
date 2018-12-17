# LCTF 2018 platform

LCTF 2018 比赛平台。

本项目中前端代码为webpack打包后的前端代码，前端源码参见[此项目](https://github.com/U1in/LCTF-2018-Frontend)。

## 部署

项目使用nginx+uwsgi+django部署，示例的[nginx配置文件](https://github.com/LCTF/LCTF_2018_Platform/blob/master/nginx.conf)和[uwsgi配置文件](https://github.com/LCTF/LCTF_2018_Platform/blob/master/app/backend/uwsgi.ini)都已上传。

## 食用方法

默认后台路径

```
api/admin/
```

可在app/backend/lctf2018_backend/urls.py中修改。

默认后台管理账号密码

```
admin
admin123456
```

使用时千万别忘了

```
cd app/backend
python manage.py changepassword admin
```

上题等操作都在后台进行。

Enjoy it.


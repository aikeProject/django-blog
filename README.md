#### 博客

##### 项目结构

```
|-- manage.py
    |-- backend 后台管理
    |-- cyBlog 项目配置文件
    |-- repository 数据仓库（操作数据Model）
    |-- static 静态文件
    |-- templates 模版
    |-- utils 公共文件
    |-- web 存放前端页面
    |-- db.sqlite3 数据库
    |-- README.md
```

###### 需求分析
```
|-- 报账系统
    |-- 用户：
        |-- 提交报账单
        |-- 自己报障记录
        |-- 处理者：
            |-- 查看所有人报障单
            |-- 处理报账单
                
|-- 知识库（博客系统）
    |--  主页：
         |--  展示最新文章
         |--  展示最热文章
         |--  展示评论最多文章
         |--  分类查看
    |--  个人博客：
         |--      个人博客主页
         |--      个人博客文章详细：赞，踩，评论
         |--      个人博客分类：标签、分类、时间
         |--      个人博客主题定制：后台修改
    |--  后台管理：
         |-- 个人信息管理
         |-- 个人标签
         |-- 个人分类
         |-- 个人文章        
```

###### 数据库设计

```
用户表： uid,username,pwd,email,img,
        博客表： bid,surfix,theme,title,summary, FK(用户表,unique)=OneToOne(用户表)
        互粉表： id  明星ID（用户表）   粉丝ID（用户表）
                          2                   1
                          1                   2
                          1                   3
                          5                   3
        
        
        报障单：UUID   title   detail   user（用户表）   processor（用户表 null）  status(待处理，处理中，已处理)  创建时间  处理事件
        
        
        分类表：caption  Fk(博客bid)
        
        标签表：caption  Fk(博客bid)
        
        
        文章：id,title,summary,ctime,FK(个人分类表),主站分类（choices）
        
        文章详细：detail  OneToOne(文章)
        
        文章标签关系：  文章ID   标签ID
        
        
        赞踩文章关系： 文章ID    用户ID   赞或踩（True，False）  联合唯一索引：（文章ID    用户ID ）
        
        评论表：id,content,FK(文章),FK(user),ctime,parent_comment_id
```



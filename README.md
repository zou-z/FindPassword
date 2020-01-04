# FindPassword
查看Sqlite3数据库中已经保存的已加密的密码
## (1)数据库字段
>Name char(30) primary key  
>Address text  
>User char(20)  
>Psw char(50)  
>Detail text  

表名默认为account
## (2)命令
>帮助 help  
>所有账户 all  
>搜索 find (名称)  
>解密 decode (索引) 
>添加项目 additem (名称) (地址) (用户名) (原始密码) (详细信息)  
>删除项目 rmitem (索引)  
>修改名称 update name (索引) (新的名称)  
>修改地址 update address (索引) (新的地址)  
>修改用户名 update user (索引) (新的用户名)  
>修改密码 update psw (索引) (新的原始密码)  
>修改详细信息 update detail (索引) (新的详细信息)  
>查看现在的密钥 key  
>修改密钥 newkey (新密钥)           //修改输入的密钥  
>更换密钥 rekey (旧密钥) (新密钥)   //以新密钥重新存储所有的密码,且修改输入的密钥  
>退出 exit

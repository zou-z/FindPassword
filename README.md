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
>修改密码 repsw (索引) (新的未加密密码)  
>查看现在的密钥 key  
>修改密钥 newkey (新密钥)           //修改输入的密钥  
>更换密钥 rekey (旧密钥) (新密钥)   //以新密钥重新存储所有的密码,且修改输入的密钥  
>退出 exit

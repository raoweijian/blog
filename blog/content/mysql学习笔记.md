##多字段约束
在应用中，经常会遇到一种情况：多条数据，A B两个字段不能都一样。
比如我现在有一个表 cov，用于统计各个模块每次提交代码时的增量覆盖率。那么一个模块的一个版本，就只能有一条数据
sql语句如下：

    alter table cov add constraint unique_base unique(module_name, version);

##取消约束
    alter table cov drop index unique_base;

注意这里的 unique_base 就是创建约束时起的名字

##复制数据库
有时候我们需要复制一套数据库用于测试，可以这么执行：

	mysqldump db_name -uxxx -pxxx -hxx.xx.xx.xx -P xxxx > sql

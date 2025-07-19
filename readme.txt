# 恢复到初始提交
git checkout a7edc36adb089aec678322fcdccce706828675be -- .

# 来基于该提交创建一个新分支用于修改。
git switch -c temp-rollback

这样你有了一个“备份分支”。
git commit -am "临时恢复到 add readme.txt 提交"

查看分支
git branch

彻底恢复包括未追踪文件
git clean -fd
git restore .

老版本
git checkout -- .
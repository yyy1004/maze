# 恢复到初始提交
git checkout a7edc36adb089aec678322fcdccce706828675be -- .

# 来基于该提交创建一个新分支用于修改。
git switch -c temp-rollback
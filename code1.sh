#!/bin/bash
echo "hello world"

# 变量
#varable
name="xiangsixing"
echo $name
echo ${name}
echo "hello $name"

age=40
readonly age
#age=50

age2=10
unset age2
echo $age2

# 字符串
# string

name2="japan"
echo "shite $name2"
echo 'shite $name2'

echo $name2 "is" $name
echo ${#name2}     # 长度
echo ${name2:2:3}  # 截取

# 数组
# array
ages=(11 22 33 44)
echo $ages
echo ${ages[@]}
echo ${ages[2]}
echo ${#ages}
echo ${#ages[@]}
echo ${#ages[*]}

# 运算符
a=10
b=40
echo `expr $a + $b`
echo `expr $a - $b`
echo `expr $a \* $b`
echo `expr $a / $b`


a=10
b=10
if [ $a -gt $b]
then
	echo "a>b"
else
	echo "a<=b"
fi

file="/root/b.txt"

if [ -e $file ]
then
	echo "exists"
else
	echo "not exists"
fi	

echo "hello"
echo -e "hello luhan\n"
echo -e "hello luhan\c"
echo
echo

printf "%-10s %-8s %-4s\n" 姓名 性别 体重kg  
printf "%-10s %-8s %-4.2f\n" 思聪 男 65.4321 
printf "%-10s %-8s %-4.2f\n" 宝强 男 51.4567 



#case语句
echo '输入 1 到 4 之间的数字:'
read aNum
case $aNum in
	1)  echo '你选择了 1'
	;;
	2)  echo '你选择了 2'
	;;
	3)  echo '你选择了 3'
	;;
	4)  echo '你选择了 4'
	;;
	*)  echo '你没有输入 1 到 4 之间的数字'
	;;
	sac


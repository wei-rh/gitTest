




# 循环
# for



for i in 1 2 3 4
do
	echo "i:$i"
done

ages=(10 20 40 50)
for n in ${ages[@]}
do
	echo "n:$n"
done

for i in 1 2 3 4 5 6 7
do
	if [ $i == 3 ]
	then
		break
	else
		echo "i:$i"
	fi
done

# 函数
# function
fn(){
	echo "fn function"
}
fn

fn2(){
	echo "a:"
	read a
	echo "b:"
	read b
	return `expr $a + $b`

}

fn2
echo "fn2 returnvalue:$?"

fn3(){
	echo $1
	echo $2
	echo $3
	echo $#
	echo $*
	echo $@
	return 100
}
fn3 10 20 30
echo $?

